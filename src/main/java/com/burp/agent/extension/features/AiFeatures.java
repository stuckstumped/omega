/*
 * Copyright (c) 2024. Burp AI Agent Extension
 * 
 * AI Features interface for enhanced Burp Suite capabilities
 */

package com.burp.agent.extension.features;

/**
 * Interface for AI-powered security testing features
 */
public interface AiFeatures
{
    /**
     * Analyze HTTP traffic for security issues using AI
     * 
     * @param requestData The HTTP request
     * @param responseData The HTTP response
     * @return Analysis result with findings and severity
     */
    AnalysisResult analyzeTraffic(String requestData, String responseData);

    /**
     * Generate security recommendations for a given URL
     * 
     * @param url The target URL
     * @param findings The security findings
     * @return Recommendations for remediation
     */
    String generateRecommendations(String url, java.util.List<String> findings);

    /**
     * Predict potential vulnerabilities based on pattern analysis
     * 
     * @param requestData The HTTP request
     * @return List of predicted vulnerabilities
     */
    java.util.List<String> predictVulnerabilities(String requestData);

    /**
     * Rate the security risk level of a response
     * 
     * @param responseData The HTTP response
     * @return Risk rating (1-10)
     */
    int rateRiskLevel(String responseData);

    /**
     * Result of traffic analysis
     */
    class AnalysisResult
    {
        public final java.util.List<String> findings;
        public final String severity;
        public final long timestamp;

        public AnalysisResult(java.util.List<String> findings, String severity)
        {
            this.findings = findings;
            this.severity = severity;
            this.timestamp = System.currentTimeMillis();
        }
    }
}
