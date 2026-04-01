/*
 * Copyright (c) 2024. Burp AI Agent Extension
 * 
 * Implementation of AI features using the Python agent
 */

package com.burp.agent.extension.features;

import com.google.gson.JsonObject;
import com.burp.agent.extension.AgentCommunicationBridge;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;

/**
 * AI features implementation backed by the Python agent
 */
public class AiFeaturesImpl implements AiFeatures
{
    private static final String LOG_PREFIX = "[AI Features]";

    @Override
    public AnalysisResult analyzeTraffic(String requestData, String responseData)
    {
        try
        {
            JsonObject payload = new JsonObject();
            payload.addProperty("action", "analyze_traffic");
            payload.addProperty("request", requestData);
            payload.addProperty("response", responseData);

            String result = AgentCommunicationBridge.analyzeWithAgent(payload);
            
            List<String> findings = extractFindings(requestData, responseData);
            String severity = determineSeverity(findings);

            return new AnalysisResult(findings, severity);
        }
        catch (Exception e)
        {
            return new AnalysisResult(
                List.of("Error during analysis: " + e.getMessage()),
                "ERROR"
            );
        }
    }

    @Override
    public String generateRecommendations(String url, List<String> findings)
    {
        StringBuilder recommendations = new StringBuilder();
        recommendations.append("Recommendations for ").append(url).append(":\n");

        for (String finding : findings)
        {
            recommendations.append("• ").append(getRecommendation(finding)).append("\n");
        }

        return recommendations.toString();
    }

    @Override
    public List<String> predictVulnerabilities(String requestData)
    {
        List<String> predictions = new ArrayList<>();

        // Pattern-based predictions
        if (requestData.toLowerCase().contains("union select"))
        {
            predictions.add("Potential SQL Injection vulnerability");
        }
        if (requestData.contains("javascript:") || requestData.contains("onerror="))
        {
            predictions.add("Potential XSS (Cross-Site Scripting) vulnerability");
        }
        if (requestData.contains("..") || requestData.contains("../"))
        {
            predictions.add("Potential Path Traversal vulnerability");
        }
        if (requestData.toLowerCase().contains("<xml") || requestData.toLowerCase().contains("<!entity"))
        {
            predictions.add("Potential XXE (XML External Entity) vulnerability");
        }
        if (requestData.toLowerCase().contains("admin") && requestData.toLowerCase().contains("password"))
        {
            predictions.add("Potential Hardcoded Credentials");
        }

        return predictions;
    }

    @Override
    public int rateRiskLevel(String responseData)
    {
        int risk = 1; // Base risk

        // Increase risk based on indicators
        if (responseData.contains("500") || responseData.contains("Internal Server Error"))
        {
            risk = Math.min(10, risk + 3);
        }
        if (responseData.contains("error") || responseData.contains("exception"))
        {
            risk = Math.min(10, risk + 2);
        }
        if (responseData.contains("stack trace") || responseData.contains("stackTrace"))
        {
            risk = Math.min(10, risk + 3);
        }
        if (!responseData.contains("X-Frame-Options"))
        {
            risk = Math.min(10, risk + 1);
        }
        if (!responseData.contains("Content-Security-Policy"))
        {
            risk = Math.min(10, risk + 1);
        }
        if (responseData.contains("Set-Cookie") && !responseData.contains("Secure"))
        {
            risk = Math.min(10, risk + 2);
        }

        return risk;
    }

    /**
     * Extract security findings from request/response
     */
    private List<String> extractFindings(String requestData, String responseData)
    {
        List<String> findings = new ArrayList<>();

        // Check request for issues
        if (requestData.toLowerCase().contains("password="))
        {
            findings.add("Potential password credentials in request body");
        }
        if (requestData.toLowerCase().contains("api_key") || requestData.toLowerCase().contains("apikey"))
        {
            findings.add("Potential API key in request");
        }

        // Check response for missing headers
        if (!responseData.contains("Content-Security-Policy"))
        {
            findings.add("Missing Content-Security-Policy header");
        }
        if (!responseData.contains("X-Frame-Options"))
        {
            findings.add("Missing X-Frame-Options header (Clickjacking protection)");
        }
        if (!responseData.contains("X-Content-Type-Options"))
        {
            findings.add("Missing X-Content-Type-Options header");
        }

        // Check for error information disclosure
        if (responseData.toLowerCase().contains("sql") || responseData.toLowerCase().contains("database"))
        {
            findings.add("Potential database error information disclosure");
        }

        return findings;
    }

    /**
     * Determine severity level based on findings
     */
    private String determineSeverity(List<String> findings)
    {
        if (findings.isEmpty())
        {
            return "SAFE";
        }

        int criticalCount = (int) findings.stream()
            .filter(f -> f.toLowerCase().contains("injection") || 
                        f.toLowerCase().contains("credentials") ||
                        f.toLowerCase().contains("xss"))
            .count();

        if (criticalCount > 0)
        {
            return "CRITICAL";
        }

        if (findings.size() > 3)
        {
            return "WARNING";
        }

        return "INFO";
    }

    /**
     * Get remediation recommendation for a finding
     */
    private String getRecommendation(String finding)
    {
        if (finding.contains("Content-Security-Policy"))
        {
            return "Implement Content-Security-Policy header to prevent XSS attacks";
        }
        if (finding.contains("X-Frame-Options"))
        {
            return "Add X-Frame-Options header to prevent clickjacking attacks";
        }
        if (finding.contains("password"))
        {
            return "Never transmit passwords in clear text; use HTTPS and secure authentication";
        }
        if (finding.contains("API key"))
        {
            return "Protect API keys; never expose them in requests or responses";
        }
        if (finding.contains("database"))
        {
            return "Implement proper error handling to avoid information disclosure";
        }

        return "Review and remediate this finding";
    }
}
