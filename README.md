# KIE Document Processing Web Application

A web application for Knowledge Information Extraction (KIE) from documents using NanoNets OCR-s model. Supports invoices, waybills, and various document formats with automatic key-value pair extraction.

## Features

- **Multi-format Support**: PDF, PNG, JPG, JPEG, DOCX, TXT
- **AI-Powered Extraction**: Uses NanoNets OCR-s model (3.75B parameters)
- **Multilingual**: Supports German and English documents
- **Web Interface**: Drag-and-drop file upload with real-time processing
- **REST API**: JSON-based API for programmatic access
- **Invoice-Optimized**: Pre-trained on invoice and financial documents

## Requirements

- Python 3.8+
- CUDA-compatible GPU with 20GB+ VRAM (recommended)
- 16GB+ RAM

## Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Install additional system dependencies**:
```bash
# For PDF processing
sudo apt-get install poppler-utils  # Ubuntu/Debian
brew install poppler  # macOS

# For flash attention (optional, for better performance)
pip install flash-attn --no-build-isolation
```

## Usage

### Starting the Application

```bash
python app.py
```

The application will start on `http://localhost:8000`

### Web Interface

1. Open `http://localhost:8000` in your browser
2. Upload a document (PDF, image, or text file)
3. Wait for processing to complete
4. View extracted key-value pairs in JSON format
5. Download results as JSON file

### API Endpoints

#### Upload Document
```bash
POST /upload
Content-Type: multipart/form-data

curl -X POST "http://localhost:8000/upload" \
     -F "file=@invoice.pdf"
```

#### Extract Data
```bash
POST /extract/{job_id}

curl -X POST "http://localhost:8000/extract/{job_id}"
```

#### Get Results
```bash
GET /results/{job_id}

curl "http://localhost:8000/results/{job_id}"
```

## API Response Format

```json
{
  "job_id": "uuid-string",
  "timestamp": "2024-01-15T10:30:00",
  "extracted_data": [
    {
      "invoice_number": "INV-2024-001",
      "date": "2024-01-15",
      "vendor_name": "ABC Company",
      "total_amount": "1,250.00",
      "currency": "EUR",
      "line_items": [
        {
          "description": "Product A",
          "quantity": "2",
          "unit_price": "500.00",
          "total": "1,000.00"
        }
      ]
    }
  ],
  "status": "completed"
}
```

## Model Information

- **Model**: NanoNets OCR-s (nanonets/Nanonets-OCR-s)
- **Parameters**: 3.75B
- **Base Model**: Qwen2.5-VL-3B-Instruct
- **Optimization**: BF16 precision, Flash Attention 2
- **Languages**: German, English, and 30+ other languages

## Performance

- **GPU Memory**: ~8-12GB VRAM usage
- **Processing Speed**: 5-15 seconds per document
- **Accuracy**: Optimized for invoice and financial documents

## Fine-tuning

To fine-tune the model with your sample invoices:

1. Prepare your training data in the expected format
2. Use the fine-tuning pipeline (implementation coming soon)
3. Update the model path in `nanonets_extractor.py`

## Troubleshooting

### Common Issues

1. **CUDA Out of Memory**: Reduce batch size or use CPU mode
2. **PDF Processing Error**: Install poppler-utils
3. **Model Loading Error**: Ensure sufficient disk space (5GB+)

### Performance Optimization

- Use GPU with 20GB+ VRAM for best performance
- Enable flash attention for memory efficiency
- Process documents in batches for high volume

## License

This project is for educational and research purposes. Please comply with NanoNets model license terms.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request
