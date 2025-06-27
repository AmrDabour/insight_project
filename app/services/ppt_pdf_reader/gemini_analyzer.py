import google.generativeai as genai
import json
import re
import logging
from typing import Dict, List, Any, Optional

from app.config import get_settings

settings = get_settings()
genai.configure(api_key=settings.google_ai_api_key)

logger = logging.getLogger(__name__)


class GeminiAnalyzer:
    def __init__(self):
        try:
            self.model = genai.GenerativeModel(settings.gemini_model)
            self.vision_model = genai.GenerativeModel(settings.gemini_vision_model)
            logger.info("✅ Gemini AI analyzer initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Gemini AI: {e}")
            self.model = None
            self.vision_model = None

    def analyze_document_bulk(
        self, document_data: Dict[str, Any], language: str = "arabic"
    ) -> Dict[str, Any]:
        """
        تحليل المستند بالكامل باستخدام Gemini AI
        """
        try:
            if not self.model:
                return self._create_fallback_analysis(document_data, language)

            # Prepare slides data for analysis
            slides_data = []
            for page in document_data["pages"]:
                slide_data = {
                    "slide_number": page["page_number"],
                    "title": page["title"],
                    "text": page["text"],
                    "notes": page.get("notes", ""),
                }
                slides_data.append(slide_data)

            # Create analysis prompt
            prompt = self._create_bulk_analysis_prompt(slides_data, language)

            # Get AI analysis
            response = self.model.generate_content(prompt)
            analysis_result = self._parse_bulk_analysis_response(
                response.text, language
            )

            return analysis_result

        except Exception as e:
            logger.error(f"Error in bulk analysis: {e}")
            return self._create_fallback_analysis(document_data, language)

    def _create_bulk_analysis_prompt(
        self, slides_data: List[Dict], language: str
    ) -> str:
        """إنشاء prompt شامل لتحليل جميع الشرائح"""

        # Prepare slides text
        slides_text = ""
        for slide in slides_data:
            if language == "arabic":
                slides_text += f"\n--- الشريحة {slide['slide_number']} ---\n"
                if slide["title"]:
                    slides_text += f"العنوان: {slide['title']}\n"
                if slide["text"]:
                    slides_text += f"المحتوى: {slide['text']}\n"
                if slide["notes"]:
                    slides_text += f"الملاحظات: {slide['notes']}\n"
            else:
                slides_text += f"\n--- Slide {slide['slide_number']} ---\n"
                if slide["title"]:
                    slides_text += f"Title: {slide['title']}\n"
                if slide["text"]:
                    slides_text += f"Content: {slide['text']}\n"
                if slide["notes"]:
                    slides_text += f"Notes: {slide['notes']}\n"

        # Language-specific instructions
        if language == "arabic":
            language_instruction = "اكتب الشرح باللغة العربية بوضوح ودقة. ركز على وصف محتوى الشريحة بأقل كلمات ممكنة"
            explanation_field = "وصف مختصر للشريحة"
            summary_instruction = "اكتب ملخص مختصر للعرض باللغة العربية"
            slide_type_options = "مقدمة/محتوى/خاتمة"
            importance_options = "عالي/متوسط/منخفض"

            analysis_rules = """قواعد التحليل:
1. اكتب الشرح باللغة العربية بوضوح ودقة
2. ركز على وصف محتوى الشريحة بأقل كلمات ممكنة
3. حدد النقاط الأساسية في كل شريحة
4. صنف نوع كل شريحة (مقدمة، محتوى، خاتمة، إلخ)
5. قيم أهمية كل شريحة
6. اكتب ملخص مختصر للعرض باللغة العربية
7. تأكد من أن JSON صحيح ومنسق"""

            prompt_header = f"أحلل هذا العرض التقديمي بالكامل. العرض يحتوي على {len(slides_data)} شريحة."
            json_instruction = "أعطني فقط JSON بدون أي نص إضافي."

        else:
            language_instruction = "Write brief explanations in clear English. Focus on describing slide content with minimal words"
            explanation_field = "brief description of slide content"
            summary_instruction = (
                "Write a brief summary of the entire presentation in English"
            )
            slide_type_options = "introduction/content/conclusion"
            importance_options = "high/medium/low"

            analysis_rules = """Analysis rules:
1. Write brief explanations in clear English
2. Focus on describing slide content with minimal words
3. Identify key points in each slide
4. Classify slide type (introduction, content, conclusion, etc.)
5. Assess importance level of each slide
6. Write a brief summary of the entire presentation in English
7. Ensure JSON is valid and properly formatted"""

            prompt_header = f"Analyze this presentation completely. The presentation contains {len(slides_data)} slides."
            json_instruction = "Return only JSON with no additional text."

        prompt = f"""{prompt_header}

{slides_text}

Return analysis for each slide in the following JSON format:

{{
  "presentation_summary": "Brief summary of the entire presentation",
  "total_slides": {len(slides_data)},
  "slides_analysis": [
    {{
      "slide_number": 1,
      "title": "Slide title",
      "original_text": "Original slide text",
      "explanation": "{explanation_field}",
      "key_points": ["Key point 1", "Key point 2"],
      "slide_type": "{slide_type_options}",
      "importance_level": "{importance_options}"
    }}
  ]
}}

{analysis_rules}

{json_instruction}"""

        return prompt

    def _parse_bulk_analysis_response(
        self, response_text: str, language: str
    ) -> Dict[str, Any]:
        """تحليل استجابة الذكاء الاصطناعي"""
        try:
            # Clean the response
            response_text = response_text.strip()

            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            # Parse JSON
            analysis_data = json.loads(response_text.strip())

            # Validate structure
            if "slides_analysis" not in analysis_data:
                raise ValueError("Missing slides_analysis in response")

            return analysis_data

        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {e}")
            return self._create_fallback_analysis_from_text(response_text, language)
        except Exception as e:
            logger.error(f"Analysis parsing error: {e}")
            return self._create_fallback_analysis_from_text(response_text, language)

    def _create_fallback_analysis(
        self, document_data: Dict[str, Any], language: str
    ) -> Dict[str, Any]:
        """إنشاء تحليل احتياطي في حالة فشل التحليل الأساسي"""

        if language == "arabic":
            summary_text = "تم إنشاء تحليل أساسي للمستند"
            slide_explanation_template = "هذه هي الصفحة رقم {i} من المستند."
            content_text = "محتوى الصفحة"
            slide_type = "محتوى"
            importance = "متوسط"
            slide_title_template = "الصفحة {i}"
        else:
            summary_text = "Basic analysis generated for the document"
            slide_explanation_template = "This is page number {i} of the document."
            content_text = "Page content"
            slide_type = "content"
            importance = "medium"
            slide_title_template = "Page {i}"

        fallback_data = {
            "presentation_summary": summary_text,
            "total_slides": document_data["total_pages"],
            "slides_analysis": [],
        }

        for page in document_data["pages"]:
            slide_analysis = {
                "slide_number": page["page_number"],
                "title": page["title"]
                or slide_title_template.format(i=page["page_number"]),
                "original_text": page["text"],
                "explanation": slide_explanation_template.format(i=page["page_number"]),
                "key_points": [content_text],
                "slide_type": slide_type,
                "importance_level": importance,
            }
            fallback_data["slides_analysis"].append(slide_analysis)

        return fallback_data

    def _create_fallback_analysis_from_text(
        self, response_text: str, language: str
    ) -> Dict[str, Any]:
        """إنشاء تحليل احتياطي من النص الخام"""

        if language == "arabic":
            summary = "تم تحليل المستند بنجاح"
            explanation = "تحليل أساسي للمحتوى"
        else:
            summary = "Document analyzed successfully"
            explanation = "Basic content analysis"

        return {
            "presentation_summary": summary,
            "total_slides": 1,
            "slides_analysis": [
                {
                    "slide_number": 1,
                    "title": "Analysis Result",
                    "original_text": response_text[:500],  # First 500 chars
                    "explanation": explanation,
                    "key_points": [explanation],
                    "slide_type": "content",
                    "importance_level": "medium",
                }
            ],
        }

    def extract_page_number_from_command(
        self, command: str, current_page: int, total_pages: int
    ) -> Optional[int]:
        """استخدام الذكاء الاصطناعي لاستخراج رقم الصفحة من الأمر"""

        if not self.model:
            return self._simple_page_extraction(command, current_page, total_pages)

        try:
            prompt = f"""Extract the page number from this voice/text command. Return ONLY the number, nothing else.

Command: "{command}"
Total pages available: {total_pages}
Current page: {current_page}

Navigation patterns:
- "وديني لصفحة رقم 55" → return: 55
- "اذهب للصفحة 10" → return: 10  
- "صفحة 25" → return: 25
- "Go to page 30" → return: 30
- "page 15" → return: 15
- "آخر صفحة" or "last page" → return: {total_pages}
- "أول صفحة" or "first page" → return: 1
- "التالي" or "next" → return: {min(current_page + 1, total_pages)}
- "السابق" or "previous" → return: {max(current_page - 1, 1)}

Return ONLY the page number (integer), or "none" if no valid navigation found."""

            response = self.model.generate_content(prompt)
            result = response.text.strip().lower()

            # Try to extract number
            if result.isdigit():
                return int(result)
            elif "none" in result:
                return None
            else:
                # Try to find number in response
                numbers = re.findall(r"\d+", result)
                if numbers:
                    return int(numbers[0])

            return None

        except Exception as e:
            logger.error(f"AI page extraction error: {e}")
            return self._simple_page_extraction(command, current_page, total_pages)

    def _simple_page_extraction(
        self, command: str, current_page: int, total_pages: int
    ) -> Optional[int]:
        """استخراج بسيط لرقم الصفحة بدون AI"""
        command_lower = command.lower()

        # Next/Previous commands
        if any(word in command_lower for word in ["next", "التالي", "التالية"]):
            return min(current_page + 1, total_pages)
        elif any(
            word in command_lower for word in ["previous", "prev", "السابق", "السابقة"]
        ):
            return max(current_page - 1, 1)
        elif any(word in command_lower for word in ["first", "أول", "اول", "البداية"]):
            return 1
        elif any(
            word in command_lower
            for word in ["last", "آخر", "اخر", "الأخيرة", "النهاية"]
        ):
            return total_pages

        # Extract numbers using regex
        numbers = re.findall(r"\d+", command)
        if numbers:
            try:
                page_num = int(numbers[0])
                if 1 <= page_num <= total_pages:
                    return page_num
            except ValueError:
                pass

        return None

    def analyze_page_image(self, image_base64: str, language: str = "arabic") -> str:
        """تحليل صورة الصفحة باستخدام Gemini Vision"""

        if not self.vision_model:
            return "Vision analysis not available"

        try:
            if language == "arabic":
                prompt = """حلل هذه الصورة واستخرج المحتوى الرئيسي منها.
                ركز على:
                - النصوص الموجودة
                - العناصر المرئية المهمة
                - الهيكل العام للصفحة
                
                اكتب الوصف باللغة العربية بشكل مختصر ومفيد."""
            else:
                prompt = """Analyze this image and extract the main content from it.
                Focus on:
                - Text content
                - Important visual elements
                - Overall page structure
                
                Write the description in English briefly and helpfully."""

            # Prepare image for Gemini
            parts = [
                {"text": prompt},
                {"inline_data": {"mime_type": "image/png", "data": image_base64}},
            ]

            response = self.vision_model.generate_content(parts)
            return response.text.strip()

        except Exception as e:
            logger.error(f"Vision analysis error: {e}")
            return (
                "خطأ في تحليل الصورة"
                if language == "arabic"
                else "Image analysis error"
            )
