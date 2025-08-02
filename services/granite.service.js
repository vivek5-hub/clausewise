// services/granite.service.js
const axios = require('axios');
const graniteConfig = require('../config/granite.config');

module.exports = {
  async analyzeText({ text, analysisType, confidenceThreshold }) {
    try {
      const headers = {
        'Authorization': `Bearer ${graniteConfig.apiKey}`,
        'Content-Type': 'application/json'
      };

      // Construct the prompt based on analysis type
      let prompt;
      switch(analysisType) {
        case 'contract':
          prompt = `Analyze this legal contract and identify:
                  1. Contract type
                  2. Key parties
                  3. Obligations
                  4. Termination clauses
                  5. Risk factors`;
          break;
        case 'compliance':
          prompt = `Review this document for compliance issues with:
                  1. Regulatory requirements
                  2. Industry standards
                  3. Potential violations`;
          break;
        default:
          prompt = `Provide a comprehensive analysis of this legal document`;
      }

      const payload = {
        input: text,
        parameters: {
          prompt,
          temperature: 0.7,
          max_tokens: 2000,
          confidence_threshold: confidenceThreshold
        }
      };

      const response = await axios.post(
        `${graniteConfig.apiUrl}${graniteConfig.endpoints.analyze}`,
        payload,
        { headers }
      );

      // Transform Granite API response to our frontend format
      return this.transformResponse(response.data, analysisType);

    } catch (error) {
      throw new Error(`Granite API error: ${error.response?.data?.error || error.message}`);
    }
  },

  transformResponse(data, analysisType) {
    // Extract entities with confidence scores
    const entities = data.entities?.map(entity => ({
      name: entity.text,
      type: entity.type,
      confidence: entity.confidence
    })) || [];

    // Calculate overall confidence score
    const confidenceScore = entities.length > 0 
      ? entities.reduce((sum, e) => sum + e.confidence, 0) / entities.length
      : 0.9; // Default if no entities

    // Determine risk level
    let riskLevel = 'Medium';
    if (confidenceScore > 0.85) riskLevel = 'Low';
    if (confidenceScore < 0.6) riskLevel = 'High';

    return {
      documentType: this.detectDocumentType(data.output, analysisType),
      confidenceScore,
      riskLevel,
      processingTime: data.processing_time || 0,
      entities,
      risks: this.extractRisks(data.output),
      insights: this.extractInsights(data.output),
      sentiment: this.analyzeSentiment(data.output),
      complianceScores: this.rateCompliance(data.output)
    };
  },

  // [Additional helper methods for response transformation]
  detectDocumentType(output, analysisType) { /* ... */ },
  extractRisks(output) { /* ... */ },
  extractInsights(output) { /* ... */ },
  analyzeSentiment(output) { /* ... */ },
  rateCompliance(output) { /* ... */ }
};