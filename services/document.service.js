const fs = require('fs');
const path = require('path');
const { extractText } = require('../utils/file.util');
const graniteService = require('./granite.service');
const logger = require('../utils/logger.util');

module.exports = {
  async processDocument(file, analysisType, confidenceThreshold) {
    try {
      // Save file temporarily
      const uploadDir = path.join(__dirname, '../uploads');
      if (!fs.existsSync(uploadDir)) {
        fs.mkdirSync(uploadDir, { recursive: true });
      }

      const filePath = path.join(uploadDir, file.name);
      await file.mv(filePath);

      // Extract text
      const text = await extractText(filePath);

      // Analyze with Granite
      const analysis = await graniteService.analyzeText({
        text,
        analysisType,
        confidenceThreshold
      });

      // Clean up
      fs.unlinkSync(filePath);

      return analysis;

    } catch (error) {
      logger.error(`Document processing error: ${error.message}`);
      throw error;
    }
  }
};