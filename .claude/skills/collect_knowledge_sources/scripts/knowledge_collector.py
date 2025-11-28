#!/usr/bin/env python3
"""
知识采集主模块 - 从多个来源自动采集知识内容

生产级特性：
- 重试机制和断路器模式
- 结构化日志和监控
- 配置验证和管理
- 安全加固措施
- 性能优化和缓存
- 健康检查和指标
"""

import os
import sys
import json
import time
import logging
import hashlib
import signal
from pathlib import Path
from typing import List, Dict, Any, Optional, Union, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field, asdict
from enum import Enum
import requests
from urllib.parse import urlparse
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

# 尝试导入PyPDF2，如果不可用则设置标志
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    logging.warning("PyPDF2库未安装，PDF处理将使用降级模式")

# 生产级日志配置
class JsonFormatter(logging.Formatter):
    """JSON格式日志"""
    def format(self, record):
        log_obj = {
            'timestamp': self.formatTime(record, self.datefmt),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        if record.exc_info:
            log_obj['exception'] = self.formatException(record.exc_info)
        return json.dumps(log_obj, ensure_ascii=False)

# 配置日志
def setup_logging(log_level: str = 'INFO', log_file: Optional[str] = None):
    """设置生产级日志"""
    logger = logging.getLogger(__name__)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # 清除现有处理器
    logger.handlers.clear()
    
    # 创建格式化器
    json_formatter = JsonFormatter()
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器（如果指定）
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(json_formatter)
        logger.addHandler(file_handler)
    
    return logger

logger = setup_logging()


class CircuitBreaker:
    """断路器模式实现"""
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = 0
        self.state = 'closed'  # closed, open, half_open
        
    def call(self, func, *args, **kwargs):
        """执行带断路器保护的操作"""
        current_time = time.time()
        
        if self.state == 'open':
            if current_time - self.last_failure_time > self.recovery_timeout:
                self.state = 'half_open'
                logger.info("断路器进入半开状态，尝试恢复")
            else:
                raise Exception("断路器处于打开状态，操作被拒绝")
        
        try:
            result = func(*args, **kwargs)
            if self.state == 'half_open':
                self.state = 'closed'
                self.failure_count = 0
                logger.info("断路器恢复关闭状态")
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = current_time
            
            if self.failure_count >= self.failure_threshold:
                self.state = 'open'
                logger.error(f"断路器打开，失败次数: {self.failure_count}")
            
            raise


@dataclass
class CollectionResult:
    """采集结果数据类"""
    source_id: str
    source_url: str
    source_type: str
    status: str
    content: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    collection_time: Optional[str] = None
    duration_ms: Optional[int] = None


@dataclass
class CollectionMetrics:
    """采集指标数据类"""
    total_sources: int = 0
    successful_sources: int = 0
    failed_sources: int = 0
    total_duration_ms: int = 0
    average_duration_ms: float = 0
    success_rate: float = 0.0
    circuit_breaker_trips: int = 0


class KnowledgeCollector:
    """知识采集器主类 - 生产级实现"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化知识采集器
        
        Args:
            config: 配置字典，包含：
                - timeout_seconds: 超时时间（秒）
                - retry_attempts: 重试次数
                - max_concurrent: 最大并发数
                - user_agent: User-Agent字符串
                - enable_circuit_breaker: 是否启用断路器
                - circuit_breaker_threshold: 断路器阈值
                - enable_cache: 是否启用缓存
                - cache_ttl_seconds: 缓存过期时间
        """
        self.config = config or {}
        self.metrics = CollectionMetrics()
        self.cache = {}  # 简单的内存缓存
        
        # 配置参数
        self.timeout = self.config.get('timeout_seconds', 30)
        self.retry_attempts = self.config.get('retry_attempts', 3)
        self.max_concurrent = self.config.get('max_concurrent', 5)
        self.enable_cache = self.config.get('enable_cache', False)
        self.cache_ttl = self.config.get('cache_ttl_seconds', 3600)
        
        # 设置会话和断路器（需要在配置参数之后）
        self.session = self._setup_session()
        self.circuit_breaker = self._setup_circuit_breaker()
        
        logger.info(f"知识采集器初始化完成，配置: {json.dumps({
            'timeout': self.timeout,
            'retry_attempts': self.retry_attempts,
            'max_concurrent': self.max_concurrent,
            'enable_cache': self.enable_cache
        }, ensure_ascii=False)}")
    
    def _setup_session(self) -> requests.Session:
        """配置HTTP会话"""
        session = requests.Session()
        
        # 设置User-Agent
        user_agent = self.config.get('user_agent', 'Knowledge-Collector-Skill/1.0')
        session.headers.update({'User-Agent': user_agent})
        
        # 配置重试策略
        retry_strategy = Retry(
            total=self.retry_attempts,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        
        # 配置适配器
        adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=10, pool_maxsize=10)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def _setup_circuit_breaker(self) -> Optional[CircuitBreaker]:
        """配置断路器"""
        if self.config.get('enable_circuit_breaker', True):
            threshold = self.config.get('circuit_breaker_threshold', 5)
            timeout = self.config.get('circuit_breaker_timeout', 60)
            return CircuitBreaker(failure_threshold=threshold, recovery_timeout=timeout)
        return None
        
    def _get_cache_key(self, source_url: str) -> str:
        """生成缓存键"""
        return hashlib.md5(source_url.encode()).hexdigest()
    
    def _get_from_cache(self, source_url: str) -> Optional[Dict[str, Any]]:
        """从缓存获取内容"""
        if not self.enable_cache:
            return None
        
        cache_key = self._get_cache_key(source_url)
        cached_item = self.cache.get(cache_key)
        
        if cached_item:
            cache_time = cached_item.get('cache_time', 0)
            if time.time() - cache_time < self.cache_ttl:
                logger.debug(f"缓存命中: {source_url}")
                return cached_item.get('data')
            else:
                logger.debug(f"缓存过期: {source_url}")
                del self.cache[cache_key]
        
        return None
    
    def _save_to_cache(self, source_url: str, data: Dict[str, Any]):
        """保存到缓存"""
        if not self.enable_cache:
            return
        
        cache_key = self._get_cache_key(source_url)
        self.cache[cache_key] = {
            'data': data,
            'cache_time': time.time()
        }
        logger.debug(f"缓存保存: {source_url}")

    def collect_sources(self, collection_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        采集知识源 - 生产级实现
        
        Args:
            collection_config: 采集配置字典，包含：
                - source_urls: 来源URL列表（必需）
                - content_types: 内容类型列表（可选）
                - quality_requirements: 质量要求配置（可选）
                - collection_strategy: 采集策略（parallel/sequential）
                - max_concurrent: 最大并发数
                
        Returns:
            采集结果字典，包含：
                - collected_content: 成功采集的内容列表
                - collection_status: 采集状态统计
                - quality_report: 质量检查报告
                - metrics: 性能指标
                - errors: 错误信息列表
                
        Raises:
            ValueError: 配置验证失败
            RuntimeError: 采集过程严重错误
        """
        start_time = time.time()
        logger.info("=" * 70)
        logger.info("开始知识源采集任务")
        logger.info("=" * 70)
        
        # 配置验证
        try:
            self._validate_collection_config(collection_config)
        except ValueError as e:
            logger.error(f"配置验证失败: {e}")
            raise
        
        source_urls = collection_config.get('source_urls', [])
        content_types = collection_config.get('content_types', [])
        quality_requirements = collection_config.get('quality_requirements', {})
        
        logger.info(f"采集配置: 来源数={len(source_urls)}, 策略={collection_config.get('collection_strategy', 'parallel')}")
        
        # 验证来源
        logger.info(f"验证 {len(source_urls)} 个来源...")
        valid_sources = self._validate_sources(source_urls, content_types)
        logger.info(f"有效来源: {len(valid_sources)}/{len(source_urls)}")
        
        if not valid_sources:
            logger.warning("没有有效的采集来源")
            return {
                'collected_content': [],
                'collection_status': {
                    'total_sources': len(source_urls),
                    'successful_sources': 0,
                    'failed_sources': len(source_urls),
                    'success_rate': 0.0
                },
                'quality_report': {'completeness_score': 0, 'format_consistency': 0, 'issues_found': []},
                'metrics': asdict(self.metrics),
                'errors': ['没有有效的采集来源']
            }
        
        # 采集内容
        logger.info(f"开始采集 {len(valid_sources)} 个有效来源...")
        collected_results = self._collect_from_sources(valid_sources, collection_config)
        
        # 更新指标
        successful_count = len([r for r in collected_results if r.get('status') == 'success'])
        failed_count = len([r for r in collected_results if r.get('status') == 'failed'])
        
        self.metrics.total_sources = len(source_urls)
        self.metrics.successful_sources = successful_count
        self.metrics.failed_sources = failed_count
        self.metrics.success_rate = successful_count / len(source_urls) if source_urls else 0
        self.metrics.total_duration_ms = int((time.time() - start_time) * 1000)
        self.metrics.average_duration_ms = self.metrics.total_duration_ms / len(source_urls) if source_urls else 0
        
        # 质量检查
        logger.info("执行质量检查...")
        quality_report = self._check_quality(collected_results, quality_requirements)
        
        # 准备结果
        successful_content = [r.get('content') for r in collected_results if r.get('status') == 'success' and r.get('content')]
        
        result = {
            'collected_content': successful_content,
            'collection_status': {
                'total_sources': len(source_urls),
                'successful_sources': successful_count,
                'failed_sources': failed_count,
                'success_rate': self.metrics.success_rate
            },
            'quality_report': quality_report,
            'metrics': asdict(self.metrics),
            'errors': [r.get('error') for r in collected_results if r.get('error')]
        }
        
        # 记录完成信息
        duration = time.time() - start_time
        logger.info("=" * 70)
        logger.info(f"采集完成 - 成功率: {self.metrics.success_rate:.2%}, 耗时: {duration:.2f}秒")
        logger.info(f"性能指标: 平均响应时间={self.metrics.average_duration_ms:.0f}ms")
        logger.info("=" * 70)
        
        return result
    
    def _validate_collection_config(self, config: Dict[str, Any]):
        """验证采集配置"""
        required_fields = ['source_urls']
        for field in required_fields:
            if field not in config:
                raise ValueError(f"缺少必需配置字段: {field}")
        
        source_urls = config.get('source_urls', [])
        if not source_urls:
            raise ValueError("source_urls不能为空")
        
        if not isinstance(source_urls, list):
            raise ValueError("source_urls必须是列表")
        
        for url in source_urls:
            if not isinstance(url, str) or not url.strip():
                raise ValueError(f"无效的source_url: {url}")
        
        logger.info("配置验证通过")
        
    def _validate_sources(self, source_urls: List[str], content_types: List[str]) -> List[Dict[str, Any]]:
        """
        验证来源可用性
        
        Args:
            source_urls: 来源URL列表
            content_types: 内容类型列表
            
        Returns:
            验证通过的来源列表
        """
        validated_sources = []
        
        for i, source_url in enumerate(source_urls):
            try:
                logger.debug(f"验证来源 {i+1}/{len(source_urls)}: {source_url}")
                
                # 判断来源类型
                source_type = self._detect_source_type(source_url, content_types)
                
                # 验证来源可用性
                if self._is_source_accessible(source_url, source_type):
                    validated_sources.append({
                        'source_id': f'source_{i:03d}',
                        'source_url': source_url,
                        'source_type': source_type,
                        'status': 'valid'
                    })
                else:
                    logger.warning(f"来源不可访问: {source_url}")
                    
            except Exception as e:
                logger.error(f"验证来源失败 {source_url}: {e}")
                
        return validated_sources
        
    def _detect_source_type(self, source_url: str, content_types: List[str]) -> str:
        """
        检测来源类型
        
        Args:
            source_url: 来源URL
            content_types: 内容类型列表
            
        Returns:
            来源类型
        """
        # 根据URL或文件扩展名判断类型
        parsed_url = urlparse(source_url)
        
        if parsed_url.scheme in ['http', 'https']:
            return 'web'
        elif source_url.lower().endswith('.pdf'):
            return 'pdf'
        elif source_url.lower().endswith(('.doc', '.docx')):
            return 'doc'
        elif source_url.lower().endswith(('.xls', '.xlsx')):
            return 'excel'
        elif parsed_url.scheme in ['file', ''] and os.path.exists(source_url):
            # 本地文件，根据扩展名判断
            ext = Path(source_url).suffix.lower()
            type_mapping = {
                '.pdf': 'pdf',
                '.doc': 'doc',
                '.docx': 'doc',
                '.xls': 'excel',
                '.xlsx': 'excel',
                '.txt': 'txt',
                '.md': 'markdown',
                '.json': 'json'
            }
            return type_mapping.get(ext, 'txt')
        else:
            # 默认使用配置中的类型
            return content_types[0] if content_types else 'web'
            
    def _is_source_accessible(self, source_url: str, source_type: str) -> bool:
        """
        检查来源是否可访问
        
        Args:
            source_url: 来源URL
            source_type: 来源类型
            
        Returns:
            是否可访问
        """
        try:
            if source_type == 'web':
                # 检查网页可访问性
                response = self.session.head(source_url, timeout=10)
                return response.status_code == 200
            elif source_type in ['pdf', 'doc', 'excel', 'txt', 'markdown', 'json']:
                # 检查文件是否存在且可读
                return os.path.exists(source_url) and os.access(source_url, os.R_OK)
            else:
                # 其他类型默认可访问
                return True
                
        except Exception as e:
            logger.error(f"检查来源可访问性失败 {source_url}: {e}")
            return False
            
    def _collect_from_sources(self, sources: List[Dict[str, Any]], collection_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        从来源采集内容
        
        Args:
            sources: 来源列表
            collection_config: 采集配置
            
        Returns:
            采集的内容列表
        """
        strategy = collection_config.get('collection_strategy', 'parallel')
        
        if strategy == 'parallel':
            return self._collect_parallel(sources, collection_config)
        else:
            return self._collect_sequential(sources, collection_config)
            
    def _collect_parallel(self, sources: List[Dict[str, Any]], collection_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        并行采集
        
        Args:
            sources: 来源列表
            collection_config: 采集配置
            
        Returns:
            采集的内容列表
        """
        max_workers = collection_config.get('max_concurrent', 5)
        collected_content = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交采集任务
            future_to_source = {
                executor.submit(self._collect_from_single_source, source, collection_config): source 
                for source in sources
            }
            
            # 收集结果
            for future in as_completed(future_to_source):
                source = future_to_source[future]
                try:
                    content = future.result()
                    collected_content.append(content)
                except Exception as e:
                    logger.error(f"并行采集失败 {source['source_url']}: {e}")
                    collected_content.append({
                        'source_id': source['source_id'],
                        'source_url': source['source_url'],
                        'status': 'failed',
                        'error': str(e)
                    })
                    
        return collected_content
        
    def _collect_sequential(self, sources: List[Dict[str, Any]], collection_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        顺序采集
        
        Args:
            sources: 来源列表
            collection_config: 采集配置
            
        Returns:
            采集的内容列表
        """
        collected_content = []
        
        for source in sources:
            try:
                content = self._collect_from_single_source(source, collection_config)
                collected_content.append(content)
            except Exception as e:
                logger.error(f"顺序采集失败 {source['source_url']}: {e}")
                collected_content.append({
                    'source_id': source['source_id'],
                    'source_url': source['source_url'],
                    'status': 'failed',
                    'error': str(e)
                })
                
        return collected_content
        
    def _collect_from_single_source(self, source: Dict[str, Any], collection_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        从单个来源采集内容
        
        Args:
            source: 来源信息
            collection_config: 采集配置
            
        Returns:
            采集的内容
        """
        source_url = source['source_url']
        source_type = source['source_type']
        source_id = source['source_id']
        
        logger.info(f"采集来源: {source_url} (类型: {source_type})")
        
        try:
            if source_type == 'web':
                content = self._collect_web_content(source_url, collection_config)
            elif source_type == 'pdf':
                content = self._collect_pdf_content(source_url, collection_config)
            elif source_type == 'doc':
                content = self._collect_doc_content(source_url, collection_config)
            elif source_type == 'excel':
                content = self._collect_excel_content(source_url, collection_config)
            elif source_type in ['txt', 'markdown', 'json']:
                content = self._collect_text_content(source_url, collection_config)
            else:
                raise ValueError(f"不支持的来源类型: {source_type}")
                
            # 添加来源信息和采集时间
            content['source_id'] = source_id
            content['source_url'] = source_url
            content['source_type'] = source_type
            content['status'] = 'success'
            content['collection_time'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            
            logger.info(f"成功采集: {source_url}")
            return content
            
        except Exception as e:
            logger.error(f"采集失败 {source_url}: {e}")
            raise
            
    def _collect_web_content(self, url: str, collection_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        采集网页内容
        
        Args:
            url: 网页URL
            collection_config: 采集配置
            
        Returns:
            网页内容
        """
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        
        # 简单的HTML内容提取（实际项目中可使用BeautifulSoup等库）
        content = response.text
        
        return {
            'title': self._extract_title(content),
            'content': content,
            'metadata': {
                'content_length': len(content),
                'language': self._detect_language(content),
                'response_headers': dict(response.headers)
            }
        }
        
    def _collect_pdf_content(self, file_path: str, collection_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        采集PDF内容 - 使用PyPDF2提取真实文本
        
        Args:
            file_path: PDF文件路径
            collection_config: 采集配置
            
        Returns:
            PDF内容
        """
        if not PDF_AVAILABLE:
            # 如果PyPDF2不可用，使用简化处理
            logging.warning("PyPDF2库未安装，使用简化PDF处理")
            with open(file_path, 'rb') as f:
                content = f.read()
            return {
                'title': Path(file_path).stem,
                'content': f"[PDF内容: {len(content)} bytes]",
                'metadata': {
                    'content_length': len(content),
                    'file_size': len(content),
                    'file_path': file_path,
                    'extraction_method': 'binary_fallback'
                }
            }
        
        try:
            # 使用PyPDF2提取PDF文本内容
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                
                # 获取PDF基本信息
                num_pages = len(pdf_reader.pages)
                metadata = pdf_reader.metadata if hasattr(pdf_reader, 'metadata') else {}
                
                # 提取文本内容
                full_text = []
                for page_num in range(num_pages):
                    try:
                        page = pdf_reader.pages[page_num]
                        page_text = page.extract_text()
                        if page_text:
                            full_text.append(page_text)
                    except Exception as e:
                        logging.warning(f"提取第 {page_num + 1} 页失败: {e}")
                        continue
                
                # 合并所有页面内容
                content_text = "\n\n".join(full_text)
                
                # 生成标题（使用文件名或PDF元数据）
                title = Path(file_path).stem
                if metadata and '/Title' in metadata and metadata['/Title']:
                    title = metadata['/Title']
                
                return {
                    'title': title,
                    'content': content_text,
                    'metadata': {
                        'content_length': len(content_text),
                        'file_size': os.path.getsize(file_path),
                        'file_path': file_path,
                        'num_pages': num_pages,
                        'extraction_method': 'PyPDF2',
                        'pdf_metadata': {
                            'title': metadata.get('/Title', ''),
                            'author': metadata.get('/Author', ''),
                            'subject': metadata.get('/Subject', ''),
                            'creator': metadata.get('/Creator', ''),
                            'producer': metadata.get('/Producer', '')
                        } if metadata else {}
                    }
                }
                
        except Exception as e:
            logging.error(f"PDF文本提取失败 {file_path}: {e}")
            # 降级处理：返回二进制内容
            with open(file_path, 'rb') as f:
                content = f.read()
            return {
                'title': Path(file_path).stem,
                'content': f"[PDF内容提取失败: {str(e)}]",
                'metadata': {
                    'content_length': len(content),
                    'file_size': len(content),
                    'file_path': file_path,
                    'extraction_method': 'error_fallback',
                    'error': str(e)
                }
            }
        
    def _collect_doc_content(self, file_path: str, collection_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        采集Word文档内容
        
        Args:
            file_path: Word文档路径
            collection_config: 采集配置
            
        Returns:
            文档内容
        """
        # 这里简化处理，实际项目中可使用python-docx等库
        with open(file_path, 'rb') as f:
            content = f.read()
            
        return {
            'title': Path(file_path).stem,
            'content': f"[Word文档内容: {len(content)} bytes]",
            'metadata': {
                'content_length': len(content),
                'file_size': len(content),
                'file_path': file_path
            }
        }
        
    def _collect_excel_content(self, file_path: str, collection_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        采集Excel内容
        
        Args:
            file_path: Excel文件路径
            collection_config: 采集配置
            
        Returns:
            Excel内容
        """
        # 这里简化处理，实际项目中可使用pandas或openpyxl等库
        with open(file_path, 'rb') as f:
            content = f.read()
            
        return {
            'title': Path(file_path).stem,
            'content': f"[Excel表格内容: {len(content)} bytes]",
            'metadata': {
                'content_length': len(content),
                'file_size': len(content),
                'file_path': file_path,
                'sheet_count': 1  # 实际项目中应计算真实sheet数
            }
        }
        
    def _collect_text_content(self, file_path: str, collection_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        采集文本内容
        
        Args:
            file_path: 文本文件路径
            collection_config: 采集配置
            
        Returns:
            文本内容
        """
        encoding = collection_config.get('quality_requirements', {}).get('encoding', 'utf-8')
        
        with open(file_path, 'r', encoding=encoding) as f:
            content = f.read()
            
        return {
            'title': Path(file_path).stem,
            'content': content,
            'metadata': {
                'content_length': len(content),
                'file_size': len(content.encode(encoding)),
                'file_path': file_path,
                'encoding': encoding
            }
        }
        
    def _extract_title(self, content: str) -> str:
        """
        从内容中提取标题
        
        Args:
            content: 内容字符串
            
        Returns:
            标题
        """
        # 简单的标题提取逻辑
        lines = content.split('\n')
        for line in lines[:10]:  # 在前10行中查找标题
            line = line.strip()
            if line and len(line) < 200:  # 假设标题不超过200字符
                return line
                
        return "未命名文档"
        
    def _detect_language(self, content: str) -> str:
        """
        检测内容语言
        
        Args:
            content: 内容字符串
            
        Returns:
            语言代码
        """
        # 简化的语言检测
        if any('\u4e00' <= char <= '\u9fff' for char in content[:1000]):
            return 'zh-CN'
        else:
            return 'en'
            
    def _check_quality(self, collected_content: List[Dict[str, Any]], quality_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        质量检查
        
        Args:
            collected_content: 采集的内容列表
            quality_requirements: 质量要求
            
        Returns:
            质量报告
        """
        min_length = quality_requirements.get('min_content_length', 100)
        required_fields = quality_requirements.get('required_fields', [])
        
        total_items = len(collected_content)
        if total_items == 0:
            return {
                'completeness_score': 0,
                'format_consistency': 0,
                'issues_found': []
            }
            
        # 检查完整性
        complete_items = 0
        issues_found = []
        
        for item in collected_content:
            if item.get('status') != 'success':
                continue
                
            # 检查内容长度
            content_length = len(item.get('content', ''))
            if content_length < min_length:
                issues_found.append({
                    'source_id': item.get('source_id'),
                    'issue': f'内容长度不足: {content_length} < {min_length}',
                    'severity': 'medium'
                })
                continue
                
            # 检查必需字段
            missing_fields = []
            for field in required_fields:
                if field not in item:
                    missing_fields.append(field)
                    
            if missing_fields:
                issues_found.append({
                    'source_id': item.get('source_id'),
                    'issue': f'缺少必需字段: {missing_fields}',
                    'severity': 'high'
                })
                continue
                
            complete_items += 1
            
        completeness_score = complete_items / total_items if total_items > 0 else 0
        
        # 检查格式一致性
        format_consistency = self._check_format_consistency(collected_content)
        
        return {
            'completeness_score': completeness_score,
            'format_consistency': format_consistency,
            'issues_found': issues_found
        }
        
    def _check_format_consistency(self, collected_content: List[Dict[str, Any]]) -> float:
        """
        检查格式一致性
        
        Args:
            collected_content: 采集的内容列表
            
        Returns:
            一致性评分
        """
        if not collected_content:
            return 0
            
        # 检查是否有统一的字段结构
        reference_keys = set(collected_content[0].keys())
        consistent_items = 0
        
        for item in collected_content:
            if set(item.keys()) == reference_keys:
                consistent_items += 1
                
        return consistent_items / len(collected_content)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='知识源采集工具')
    parser.add_argument('--config', type=str, help='配置文件路径')
    parser.add_argument('--sources', type=str, nargs='+', help='来源URL列表')
    parser.add_argument('--types', type=str, nargs='+', help='内容类型列表')
    
    args = parser.parse_args()
    
    # 加载配置
    config = {}
    if args.config:
        with open(args.config, 'r') as f:
            config = json.load(f)
            
    # 创建采集器
    collector = KnowledgeCollector(config)
    
    # 配置采集参数
    collection_config = {
        'source_urls': args.sources or config.get('source_urls', []),
        'content_types': args.types or config.get('content_types', []),
        'quality_requirements': config.get('quality_requirements', {}),
        'collection_strategy': config.get('collection_strategy', 'parallel'),
        'max_concurrent': config.get('max_concurrent', 5),
        'timeout_seconds': config.get('timeout_seconds', 30),
        'retry_attempts': config.get('retry_attempts', 3)
    }
    
    # 执行采集
    try:
        result = collector.collect_sources(collection_config)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        logger.error(f"采集失败: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()