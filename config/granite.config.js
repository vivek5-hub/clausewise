module.exports = {
  apiKey: process.env.IBM_GRANITE_API_KEY,
  apiUrl: process.env.IBM_GRANITE_API_URL || 'https://api.ibm.com/granite/v1',
  endpoints: {
    analyze: '/analyze',
    entities: '/entities',
    sentiment: '/sentiment'
  }
};