#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import glob
import json
import logging
from typing import Dict, List, Tuple, Any
from collections import defaultdict

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.tokenize import sent_tokenize
from rouge import Rouge

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 初始化NLTK数据
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# 初始化Rouge
rouge = Rouge()

class ReadmeEvaluator:
    """README文档评估类"""
    
    # 评分标准权重
    WEIGHTS = {
        'content_similarity': 0.3,  # 内容相似度
        'structure_similarity': 0.2,  # 结构相似度
        'information_coverage': 0.3,  # 信息覆盖度
        'language_quality': 0.2,  # 语言质量
    }
    
    # 核心README章节（按重要性排序）
    CORE_SECTIONS = [
        '项目描述', '简介', 'introduction', 'description', 
        '安装', '使用', 'installation', 'usage',
        '功能', '特性', 'features', 
        '示例', 'examples',
        '配置', 'configuration',
        '架构', 'architecture',
        '开发', 'development',
        '贡献', 'contributing',
        '许可证', 'license'
    ]
    
    def __init__(self):
        """初始化评估器"""
        self.vectorizer = TfidfVectorizer(
            min_df=2, max_df=0.95,
            stop_words='english',
            token_pattern=r'\b[\w\u4e00-\u9fa5]+\b'  # 支持中英文词语
        )
    
    def evaluate_folder(self, folder_path: str) -> Dict[str, Any]:
        """
        评估指定目录下的README文档对
        
        Args:
            folder_path: 评估目录路径
            
        Returns:
            Dict[str, Any]: 评估结果
        """
        logger.info(f"开始评估目录: {folder_path}")
        
        # 寻找原始README和生成的README
        original_readme = self._find_file(folder_path, "README.md")
        generated_readme = self._find_file(folder_path, "README_4omini.md")
        
        if not original_readme or not generated_readme:
            logger.warning(f"目录 {folder_path} 中未找到完整的README对")
            return {
                "folder": os.path.basename(folder_path),
                "error": "未找到完整的README对",
                "score": 0
            }
        
        # 读取文件内容
        original_content = self._read_file(original_readme)
        generated_content = self._read_file(generated_readme)
        
        if not original_content or not generated_content:
            logger.warning(f"目录 {folder_path} 中的README文件内容为空")
            return {
                "folder": os.path.basename(folder_path),
                "error": "README文件内容为空",
                "score": 0
            }
        
        # 计算各项指标
        metrics = {
            'content_similarity': self._calculate_content_similarity(original_content, generated_content),
            'structure_similarity': self._calculate_structure_similarity(original_content, generated_content),
            'information_coverage': self._calculate_information_coverage(original_content, generated_content),
            'language_quality': self._calculate_language_quality(generated_content)
        }
        
        # 计算加权分数
        weighted_score = sum(
            score * self.WEIGHTS[metric]
            for metric, score in metrics.items()
        )
        
        # 四舍五入到2位小数
        weighted_score = round(weighted_score, 2)
        
        return {
            "folder": os.path.basename(folder_path),
            "original_readme": original_readme,
            "generated_readme": generated_readme,
            "metrics": {k: round(v, 2) for k, v in metrics.items()},
            "score": weighted_score
        }
    
    def evaluate_all(self, root_dir: str = "examples") -> Dict[str, Any]:
        """
        评估所有示例目录
        
        Args:
            root_dir: 包含所有示例的根目录
            
        Returns:
            Dict[str, Any]: 所有评估结果
        """
        # 查找所有子目录
        examples_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), root_dir)
        subdirs = [d for d in glob.glob(os.path.join(examples_dir, "*")) if os.path.isdir(d)]
        
        if not subdirs:
            logger.warning(f"在 {examples_dir} 中未找到示例目录")
            return {"error": f"在 {examples_dir} 中未找到示例目录"}
        
        # 评估每个子目录
        results = []
        for subdir in subdirs:
            result = self.evaluate_folder(subdir)
            results.append(result)
        
        # 计算平均分
        valid_scores = [r["score"] for r in results if "error" not in r]
        avg_score = sum(valid_scores) / len(valid_scores) if valid_scores else 0
        
        # 计算各指标的平均分
        avg_metrics = defaultdict(float)
        for result in results:
            if "metrics" in result:
                for metric, score in result["metrics"].items():
                    avg_metrics[metric] += score / len(valid_scores)
        
        # 总结结果
        summary = {
            "total_evaluated": len(subdirs),
            "valid_evaluations": len(valid_scores),
            "average_score": round(avg_score, 2),
            "average_metrics": {k: round(v, 2) for k, v in avg_metrics.items()},
            "results": results
        }
        
        return summary
    
    def _find_file(self, folder_path: str, filename: str) -> str:
        """
        在目录中查找指定文件
        
        Args:
            folder_path: 目录路径
            filename: 文件名
            
        Returns:
            str: 文件路径，若未找到则返回空字符串
        """
        filepath = os.path.join(folder_path, filename)
        return filepath if os.path.exists(filepath) else ""
    
    def _read_file(self, filepath: str) -> str:
        """
        读取文件内容
        
        Args:
            filepath: 文件路径
            
        Returns:
            str: 文件内容
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"读取文件 {filepath} 失败: {str(e)}")
            return ""
    
    def _calculate_content_similarity(self, original: str, generated: str) -> float:
        """
        计算内容相似度，使用TF-IDF和余弦相似度
        
        Args:
            original: 原始README内容
            generated: 生成的README内容
            
        Returns:
            float: 内容相似度得分 (0-1)
        """
        try:
            # 创建一个只针对当前两个文档的向量器，参数更宽松
            vectorizer = TfidfVectorizer(
                min_df=1,  # 改为1，允许词语只出现一次
                max_df=1.0,  # 改为1.0，允许词语出现在所有文档中
                stop_words='english',
                token_pattern=r'\b[\w\u4e00-\u9fa5]+\b'  # 支持中英文词语
            )
            
            # 转换为TF-IDF向量
            tfidf_matrix = vectorizer.fit_transform([original, generated])
            
            # 计算余弦相似度
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            # ROUGE-L得分（长序列匹配）
            try:
                rouge_scores = rouge.get_scores(generated, original)[0]
                rouge_l_score = rouge_scores['rouge-l']['f']
            except:
                rouge_l_score = 0
            
            # 综合得分（TF-IDF和ROUGE-L的加权平均）
            score = 0.7 * similarity + 0.3 * rouge_l_score
            
            return min(1.0, score)
        except Exception as e:
            logger.error(f"计算内容相似度失败: {str(e)}")
            return 0.0
    
    def _calculate_structure_similarity(self, original: str, generated: str) -> float:
        """
        计算结构相似度，比较文档结构（标题和章节）
        
        Args:
            original: 原始README内容
            generated: 生成的README内容
            
        Returns:
            float: 结构相似度得分 (0-1)
        """
        try:
            # 提取标题
            original_headers = self._extract_headers(original)
            generated_headers = self._extract_headers(generated)
            
            if not original_headers or not generated_headers:
                return 0.5  # 如果任一文档没有提取到标题，给予中等分数
            
            # 计算标题级别分布的相似度
            original_level_counts = self._count_header_levels(original_headers)
            generated_level_counts = self._count_header_levels(generated_headers)
            
            level_similarity = 1.0 - sum(
                abs(original_level_counts.get(level, 0) - generated_level_counts.get(level, 0)) 
                for level in set(original_level_counts) | set(generated_level_counts)
            ) / max(sum(original_level_counts.values()), sum(generated_level_counts.values()), 1)
            
            # 计算标题内容相似度
            original_header_texts = [h[1].lower() for h in original_headers]
            generated_header_texts = [h[1].lower() for h in generated_headers]
            
            # 计算相似标题的比例
            matched_headers = 0
            for gen_header in generated_header_texts:
                for orig_header in original_header_texts:
                    # 检查两个标题是否相似
                    if self._text_similarity(gen_header, orig_header) > 0.7:
                        matched_headers += 1
                        break
            
            content_similarity = matched_headers / len(generated_header_texts) if generated_header_texts else 0
            
            # 综合得分
            score = 0.5 * level_similarity + 0.5 * content_similarity
            
            return score
        except Exception as e:
            logger.error(f"计算结构相似度失败: {str(e)}")
            return 0.0
    
    def _calculate_information_coverage(self, original: str, generated: str) -> float:
        """
        计算信息覆盖度，评估生成的README是否包含原始README中的关键信息
        
        Args:
            original: 原始README内容
            generated: 生成的README内容
            
        Returns:
            float: 信息覆盖度得分 (0-1)
        """
        try:
            # 检查核心章节的覆盖情况
            original_sections = self._extract_sections(original)
            generated_sections = self._extract_sections(generated)
            
            # 如果没有识别到章节，直接比较全文相似度
            if len(original_sections) <= 1 or "_main" in original_sections:
                logger.info("无法识别章节，使用全文相似度评估")
                return self._calculate_content_similarity(original, generated)
            
            # 检查每个核心章节是否被覆盖
            core_section_coverage = 0
            core_sections_found = 0
            
            # 更宽松地匹配核心章节
            matched_sections = {}
            for section_name, section_content in original_sections.items():
                # 查找原始README中的核心章节
                for core in self.CORE_SECTIONS:
                    if core.lower() in section_name.lower():
                        core_sections_found += 1
                        matched_sections[section_name] = section_content
                        break
            
            # 如果没有找到核心章节，把所有章节都视为重要章节
            if core_sections_found == 0:
                logger.info("未找到核心章节，使用所有章节评估")
                matched_sections = original_sections
                core_sections_found = len(matched_sections)
            
            logger.info(f"找到 {core_sections_found} 个核心章节")
            
            # 判断每个章节的覆盖情况
            for section_name, section_content in matched_sections.items():
                # 首先尝试找到完全匹配的章节
                section_covered = False
                for gen_name, gen_content in generated_sections.items():
                    # 检查章节名称是否相似
                    if self._text_similarity(section_name, gen_name) > 0.6:
                        # 计算章节内容的相似度
                        section_similarity = max(
                            self._text_similarity(section_content, gen_content),
                            self._semantic_similarity(section_content, gen_content)
                        )
                        logger.info(f"章节 '{section_name}' 与 '{gen_name}' 的相似度: {section_similarity:.2f}")
                        if section_similarity > 0.4:  # 降低阈值
                            core_section_coverage += section_similarity  # 使用相似度作为分数
                            section_covered = True
                            break
                
                # 如果在生成的README中找不到对应章节，在全文中搜索关键信息
                if not section_covered:
                    # 提取原始章节中的关键句子
                    key_sentences = self._extract_key_sentences(section_content, top_n=min(5, len(section_content.split('.')) // 2 + 1))
                    
                    if key_sentences:
                        matches = 0
                        for sentence in key_sentences:
                            # 在所有生成的内容中查找相似句子
                            gen_text = " ".join(gen_content for gen_content in generated_sections.values())
                            if self._contains_similar_sentence(gen_text, sentence, threshold=0.5):  # 降低阈值
                                matches += 1
                        
                        match_ratio = matches / len(key_sentences)
                        logger.info(f"章节 '{section_name}' 的关键句子匹配率: {match_ratio:.2f}")
                        if match_ratio > 0:
                            core_section_coverage += match_ratio * 0.8  # 给予部分分数
            
            # 计算核心章节覆盖率，确保分数在合理范围内
            section_coverage_score = min(1.0, core_section_coverage / core_sections_found) if core_sections_found > 0 else 0.5
            logger.info(f"章节覆盖得分: {section_coverage_score:.2f}")
            
            # 检查关键术语覆盖率
            original_terms = self._extract_key_terms(original)
            generated_terms = self._extract_key_terms(generated)
            
            logger.info(f"原始README中提取到 {len(original_terms)} 个关键术语")
            logger.info(f"生成的README中提取到 {len(generated_terms)} 个关键术语")
            
            # 计算关键术语匹配率
            matched_terms = 0
            for term in original_terms:
                if any(self._text_similarity(term, gen_term) > 0.7 for gen_term in generated_terms):
                    matched_terms += 1
            
            term_coverage_score = matched_terms / len(original_terms) if original_terms else 0.5
            logger.info(f"术语覆盖得分: {term_coverage_score:.2f} ({matched_terms}/{len(original_terms)})")
            
            # 综合得分
            score = 0.7 * section_coverage_score + 0.3 * term_coverage_score
            
            return score
        except Exception as e:
            logger.error(f"计算信息覆盖度失败: {str(e)}")
            return 0.3  # 出错时给予一个中低分而不是0分
    
    def _calculate_language_quality(self, content: str) -> float:
        """
        评估语言质量
        
        Args:
            content: README内容
            
        Returns:
            float: 语言质量得分 (0-1)
        """
        try:
            # 分割句子
            sentences = sent_tokenize(content)
            
            if not sentences:
                return 0.5
            
            # 计算平均句子长度
            avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
            
            # 理想的平均句子长度在10-25之间
            sentence_length_score = 1.0 - min(1.0, abs(avg_sentence_length - 17.5) / 15)
            
            # 检查格式一致性
            format_consistency = self._check_format_consistency(content)
            
            # 检查代码块和链接的正确性
            code_blocks_score = self._check_code_blocks(content)
            links_score = self._check_links(content)
            
            # 综合得分
            score = (0.4 * sentence_length_score + 
                    0.3 * format_consistency + 
                    0.15 * code_blocks_score + 
                    0.15 * links_score)
            
            return score
        except Exception as e:
            logger.error(f"计算语言质量失败: {str(e)}")
            return 0.5
    
    def _extract_headers(self, text: str) -> List[Tuple[int, str]]:
        """
        提取文档中的标题
        
        Args:
            text: Markdown文本
            
        Returns:
            List[Tuple[int, str]]: 标题列表，每项包含级别和文本
        """
        # 匹配Markdown标题
        header_pattern = re.compile(r'^(#{1,6})\s+(.+?)(?:\s+#{1,6})?$', re.MULTILINE)
        headers = [(len(m.group(1)), m.group(2).strip()) for m in header_pattern.finditer(text)]
        return headers
    
    def _count_header_levels(self, headers: List[Tuple[int, str]]) -> Dict[int, int]:
        """
        计算各级标题的数量
        
        Args:
            headers: 标题列表
            
        Returns:
            Dict[int, int]: 各级标题数量
        """
        counts = defaultdict(int)
        for level, _ in headers:
            counts[level] += 1
        return counts
    
    def _extract_sections(self, text: str) -> Dict[str, str]:
        """
        提取文档中的章节
        
        Args:
            text: Markdown文本
            
        Returns:
            Dict[str, str]: 章节名称到内容的映射
        """
        # 提取标题
        headers = self._extract_headers(text)
        if not headers:
            return {"_main": text}
        
        # 按照在文档中的位置排序
        header_positions = []
        current_pos = 0
        for match in re.finditer(r'^(#{1,6})\s+(.+?)(?:\s+#{1,6})?$', text, re.MULTILINE):
            header_positions.append((match.start(), match.group(1), match.group(2).strip()))
        
        # 构建章节
        sections = {}
        for i, (pos, level, header) in enumerate(header_positions):
            end_pos = header_positions[i+1][0] if i < len(header_positions) - 1 else len(text)
            section_content = text[pos + len(level) + len(header) + 1:end_pos].strip()
            sections[header] = section_content
        
        return sections
    
    def _extract_key_sentences(self, text: str, top_n: int = 3) -> List[str]:
        """
        提取文本中的关键句子
        
        Args:
            text: 文本内容
            top_n: 提取的关键句子数量
            
        Returns:
            List[str]: 关键句子列表
        """
        sentences = sent_tokenize(text)
        if len(sentences) <= top_n:
            return sentences
        
        # 简单地选择前N个句子作为关键句子
        # 在实际应用中，可以使用更复杂的重要性评分
        return sentences[:top_n]
    
    def _contains_similar_sentence(self, text: str, sentence: str, threshold: float = 0.7) -> bool:
        """
        检查文本是否包含与给定句子相似的句子
        
        Args:
            text: 要搜索的文本
            sentence: 目标句子
            threshold: 相似度阈值
            
        Returns:
            bool: 是否包含相似句子
        """
        text_sentences = sent_tokenize(text)
        return any(self._text_similarity(s, sentence) > threshold for s in text_sentences)
    
    def _text_similarity(self, text1: str, text2: str) -> float:
        """
        计算两段文本的相似度
        
        Args:
            text1: 第一段文本
            text2: 第二段文本
            
        Returns:
            float: 相似度得分 (0-1)
        """
        # 使用简单的Jaccard相似度
        if not text1 or not text2:
            return 0.0
            
        set1 = set(self._tokenize(text1.lower()))
        set2 = set(self._tokenize(text2.lower()))
        
        if not set1 or not set2:
            return 0.0
            
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        
        return len(intersection) / len(union)
    
    def _tokenize(self, text: str) -> List[str]:
        """
        将文本分词
        
        Args:
            text: 文本内容
            
        Returns:
            List[str]: 词语列表
        """
        # 支持中英文分词
        return re.findall(r'\b[\w\u4e00-\u9fa5]+\b', text)
    
    def _extract_key_terms(self, text: str, top_n: int = 20) -> List[str]:
        """
        提取文本中的关键术语
        
        Args:
            text: 文本内容
            top_n: 提取的关键术语数量
            
        Returns:
            List[str]: 关键术语列表
        """
        extracted_terms = []
        
        # 1. 提取代码引用中的术语
        code_terms = re.findall(r'`([^`]+)`', text)
        extracted_terms.extend(code_terms)
        
        # 2. 提取引号中的术语
        quoted_terms = re.findall(r'"([^"]+)"|\'([^\']+)\'', text)
        for qt in quoted_terms:
            term = ''.join(t for t in qt if t)
            if term:
                extracted_terms.append(term)
        
        # 3. 提取中文引号和括号中的术语
        chinese_quoted = re.findall(r'[""]([^""]+)["""]|['']([^'']+)['']|「([^」]+)」|（([^）]+)）', text)
        for cq in chinese_quoted:
            term = ''.join(t for t in cq if t)
            if term:
                extracted_terms.append(term)
        
        # 4. 提取驼峰命名的词语
        camel_case = re.findall(r'\b([A-Z][a-z0-9]+([A-Z][a-z0-9]+)+)\b', text)
        extracted_terms.extend(t[0] for t in camel_case if t[0])
        
        # 5. 提取全大写的词语（可能是缩写）
        upper_case = re.findall(r'\b([A-Z]{2,})\b', text)
        extracted_terms.extend(upper_case)
        
        # 6. 尝试提取中文专有名词（3个或更多连续的中文字符）
        chinese_phrases = re.findall(r'[\u4e00-\u9fa5]{3,}', text)
        extracted_terms.extend(chinese_phrases)
        
        # 过滤并去重
        filtered_terms = []
        for term in extracted_terms:
            term = term.strip()
            if term and len(term) >= 2 and term not in filtered_terms:
                filtered_terms.append(term)
        
        # 如果提取的术语太少，尝试从长句子中提取名词短语
        if len(filtered_terms) < 5:
            sentences = sent_tokenize(text)
            for sentence in sentences:
                if len(sentence.split()) > 5:  # 只处理较长的句子
                    words = self._tokenize(sentence)
                    # 简单地提取连续的2-3个词作为可能的术语
                    for i in range(len(words) - 1):
                        if len(words[i]) > 1 and len(words[i+1]) > 1:
                            term = words[i] + " " + words[i+1]
                            if term not in filtered_terms:
                                filtered_terms.append(term)
        
        return filtered_terms[:top_n]
    
    def _check_format_consistency(self, text: str) -> float:
        """
        检查格式一致性
        
        Args:
            text: Markdown文本
            
        Returns:
            float: 格式一致性得分 (0-1)
        """
        # 检查标题格式一致性
        headers = self._extract_headers(text)
        if not headers:
            return 0.5
        
        # 检查标题级别是否适当递增
        level_errors = 0
        prev_level = 0
        for level, _ in headers:
            if prev_level > 0 and level > prev_level + 1:
                level_errors += 1
            prev_level = level
        
        level_consistency = 1.0 - min(1.0, level_errors / len(headers))
        
        # 检查列表格式一致性
        list_pattern = re.compile(r'^(\s*[-*+]|\s*\d+\.)\s+', re.MULTILINE)
        list_items = list_pattern.findall(text)
        
        list_types = {}
        for item in list_items:
            item_type = 'bullet' if re.match(r'\s*[-*+]', item) else 'numbered'
            indent = len(item) - len(item.lstrip())
            list_types[(indent, item_type)] = list_types.get((indent, item_type), 0) + 1
        
        list_consistency = 1.0 if not list_items else max(
            list_types.values()) / len(list_items)
        
        # 综合得分
        return 0.7 * level_consistency + 0.3 * list_consistency
    
    def _check_code_blocks(self, text: str) -> float:
        """
        检查代码块的正确性
        
        Args:
            text: Markdown文本
            
        Returns:
            float: 代码块正确性得分 (0-1)
        """
        # 检查代码块是否正确闭合
        code_block_starts = len(re.findall(r'```(?:[a-zA-Z0-9]+)?\s*$', text, re.MULTILINE))
        code_block_ends = len(re.findall(r'```\s*$', text, re.MULTILINE))
        
        if code_block_starts == 0 and code_block_ends == 0:
            return 1.0  # 没有代码块视为正确
        
        if code_block_starts != code_block_ends:
            return 0.5  # 代码块不匹配
        
        # 检查代码块是否指定了语言
        code_blocks_with_lang = len(re.findall(r'```[a-zA-Z0-9]+\s*$', text, re.MULTILINE))
        lang_consistency = code_blocks_with_lang / code_block_starts if code_block_starts > 0 else 1.0
        
        return 0.5 + 0.5 * lang_consistency
    
    def _check_links(self, text: str) -> float:
        """
        检查链接的正确性
        
        Args:
            text: Markdown文本
            
        Returns:
            float: 链接正确性得分 (0-1)
        """
        # 查找所有链接
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', text)
        
        if not links:
            return 1.0  # 没有链接视为正确
        
        # 检查链接格式是否正确
        invalid_links = 0
        for _, url in links:
            if not url or url.isspace():
                invalid_links += 1
        
        return 1.0 - min(1.0, invalid_links / len(links))
    
    def _semantic_similarity(self, text1: str, text2: str) -> float:
        """
        计算两段文本的语义相似度
        
        Args:
            text1: 第一段文本
            text2: 第二段文本
            
        Returns:
            float: 语义相似度得分 (0-1)
        """
        # 这是一个简化的语义相似度计算，基于关键词覆盖率
        try:
            # 提取两段文本的关键词
            words1 = set(self._tokenize(text1.lower()))
            words2 = set(self._tokenize(text2.lower()))
            
            # 过滤掉太短的词
            words1 = {w for w in words1 if len(w) > 2}
            words2 = {w for w in words2 if len(w) > 2}
            
            if not words1 or not words2:
                return 0.0
            
            # 计算第一段文本中的关键词在第二段文本中的覆盖率
            words_in_common = words1.intersection(words2)
            coverage = len(words_in_common) / len(words1)
            
            return coverage
        except Exception as e:
            logger.error(f"计算语义相似度失败: {str(e)}")
            return 0.0


def main():
    """主函数"""
    # 创建评估器
    evaluator = ReadmeEvaluator()
    
    # 评估所有示例
    results = evaluator.evaluate_all()
    
    # 打印评估结果
    print("\n========== README评估结果 ==========")
    print(f"评估的README对数量: {results['valid_evaluations']}/{results['total_evaluated']}")
    print(f"平均得分: {results['average_score']} / 1.0")
    print("\n各指标平均分:")
    for metric, score in results['average_metrics'].items():
        print(f"  - {metric}: {score}")
    
    print("\n各项目评估结果:")
    for result in results['results']:
        print(f"\n{result['folder']}:")
        if "error" in result:
            print(f"  错误: {result['error']}")
        else:
            print(f"  总得分: {result['score']} / 1.0")
            print("  各指标得分:")
            for metric, score in result['metrics'].items():
                print(f"    - {metric}: {score}")
    
    # 保存评估结果到文件
    result_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "evaluation_results.json")
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n评估结果已保存到: {result_file}")


if __name__ == "__main__":
    main()