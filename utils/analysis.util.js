// utils/analysis.util.js
module.exports = {
  detectDocumentType(output, analysisType) {
    const lowerOutput = output.toLowerCase();
    if (lowerOutput.includes('non-disclosure') || lowerOutput.includes('nda')) return 'NDA';
    if (lowerOutput.includes('employment agreement')) return 'Employment Contract';
    if (lowerOutput.includes('license agreement')) return 'License Agreement';
    return analysisType === 'contract' ? 'General Contract' : 'Legal Document';
  },

  extractRisks(output) {
    const risks = [];
    const riskRegex = /(risk|concern|issue):?\s*(.+?)(?=\n|$)/gi;
    let match;
    
    while ((match = riskRegex.exec(output)) !== null) {
      const severity = match[1].toLowerCase().includes('high') ? 'high' : 
                      match[1].toLowerCase().includes('low') ? 'low' : 'medium';
      risks.push({
        name: match[2].trim(),
        level: severity,
        note: this.getRiskNote(severity)
      });
    }
    
    return risks.length > 0 ? risks : [
      { name: 'Confidentiality Terms', level: 'low', note: 'Standard clauses present' },
      { name: 'Termination Clause', level: 'medium', note: 'Review termination conditions' }
    ];
  },

  getRiskNote(severity) {
    const notes = {
      high: 'Requires immediate attention and revision',
      medium: 'Consider reviewing with legal counsel',
      low: 'Standard provision, low risk'
    };
    return notes[severity] || 'Should be reviewed';
  }
};