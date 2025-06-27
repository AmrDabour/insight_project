# AI Models Directory

This directory contains the AI models required for the Insight Project services.

## YOLO Models for Form Reader

### boxes.pt (15MB)
- **Purpose**: Detects form fields, checkboxes, and other form elements
- **Service**: Form Reader
- **Required**: Yes (for form analysis functionality)
- **Type**: YOLOv8 model

### dot_line.pt (6MB)  
- **Purpose**: Detects dotted lines and form boundaries
- **Service**: Form Reader
- **Required**: Yes (for form structure analysis)
- **Type**: YOLOv8 model

## Important Notes

⚠️ **These model files are essential for cloud deployment**
- They are included in the repository despite their size
- Required for Form Reader service to function properly
- Do NOT remove these files when deploying to cloud platforms

## Model Training

These models were trained specifically for form analysis tasks:
- Arabic and English form support
- Various form layouts and styles
- High accuracy for document processing

## Usage

The models are automatically loaded by the Form Reader service when:
- Processing uploaded form images
- Detecting form fields and structures
- Extracting text from form elements

## Technical Specifications

- **Framework**: YOLOv8
- **Input Size**: Variable (auto-resized)
- **Output**: Bounding boxes with confidence scores
- **Classes**: Form fields, checkboxes, text areas, etc. 