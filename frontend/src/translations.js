// Simple translation function
export const t = (key, language = 'en') => {
  const translations = {
    en: {
      brand: 'FinSight AI',
      brandSubtitle: 'SME Financial Intelligence Platform',
      dashboard: 'Overview',
      analysis: 'Analysis',
      reports: 'Reports',
      totalRevenue: 'Total Revenue',
      netProfit: 'Net Profit',
      profitMargin: 'Profit Margin',
      creditScore: 'Credit Score',
      totalRevenueDesc: 'Net profit as a percentage of revenue. Industry benchmark: 10-15%',
      netProfitDesc: 'Revenue minus all expenses and taxes',
      profitMarginDesc: 'Net profit as a percentage of revenue',
      creditScoreDesc: 'Overall creditworthiness based on financial health',
      loading: 'Loading',
      error: 'Error',
    },
    hi: {
      brand: 'फिनसाइट एआई',
      brandSubtitle: 'एसएमई वित्तीय खुफिया मंच',
      dashboard: 'अवलोकन',
      analysis: 'विश्लेषण',
      reports: 'रिपोर्ट',
      totalRevenue: 'कुल राजस्व',
      netProfit: 'शुद्ध लाभ',
      profitMargin: 'लाभ मार्जिन',
      creditScore: 'क्रेडिट स्कोर',
      loading: 'लोड हो रहा है',
      error: 'त्रुटि',
    },
  };

  return translations[language]?.[key] || translations.en[key] || key;
};

export default { t };