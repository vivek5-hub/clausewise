const fs = require('fs').promises;
const pdf = require('pdf-parse');
const mammoth = require('mammoth');

module.exports = {
  async extractText(filePath) {
    try {
      const ext = filePath.split('.').pop().toLowerCase();

      if (ext === 'pdf') {
        const dataBuffer = await fs.readFile(filePath);
        const data = await pdf(dataBuffer);
        return data.text;
      } 
      else if (ext === 'docx') {
        const result = await mammoth.extractRawText({ path: filePath });
        return result.value;
      }
      else if (ext === 'txt' || ext === 'doc') {
        return fs.readFile(filePath, 'utf8');
      }
      else {
        throw new Error('Unsupported file format');
      }
    } catch (error) {
      throw new Error(`Text extraction failed: ${error.message}`);
    }
  }
};