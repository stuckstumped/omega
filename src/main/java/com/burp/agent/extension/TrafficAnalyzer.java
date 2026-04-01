/*
 * Copyright (c) 2024. Burp AI Agent Extension
 * 
 * Traffic analyzer for processing HTTP requests and responses
 */

package com.burp.agent.extension;

import burp.api.montoya.http.handler.HttpHandlerRequestResponse;
import burp.api.montoya.http.message.HttpRequestResponse;
import com.burp.agent.extension.api.MessageReceivedAction;
import com.burp.agent.extension.api.MessageToBeSentAction;
import com.burp.agent.extension.features.AiFeatures;
import com.burp.agent.extension.features.AiFeaturesImpl;
import com.google.gson.JsonObject;

/**
 * Analyzes HTTP traffic and makes AI-driven decisions about message handling
 * Uses MessageReceivedAction and MessageToBeSentAction enums to control proxy behavior
 */
public class TrafficAnalyzer
{
    private static final AiFeatures aiFeatures = new AiFeaturesImpl();
    private static final AgentCommunicationBridge communicationBridge = new AgentCommunicationBridge();

    /**
     * Extract and analyze HTTP request/response pair
     * 
     * @param interaction HTTP request/response interaction
     * @return Analysis result from AI agent
     */
    public static String analyzeInteraction(HttpHandlerRequestResponse interaction)
    {
        try
        {
            HttpRequestResponse httpRequestResponse = interaction.requestResponse();
            
            if (httpRequestResponse == null)
            {
                return null;
            }

            String requestText = httpRequestResponse.request().bodyToString();
            String responseText = httpRequestResponse.response() != null ? 
                                 httpRequestResponse.response().bodyToString() : "";

            // Use AI features for analysis
            AiFeatures.AnalysisResult result = aiFeatures.analyzeTraffic(requestText, responseText);
            
            // Build output
            StringBuilder output = new StringBuilder();
            output.append("Severity: ").append(result.severity).append("\n");
            output.append("Findings: ").append(result.findings.size()).append("\n");
            for (String finding : result.findings)
            {
                output.append("  - ").append(finding).append("\n");
            }

            // Get recommendations
            String recommendations = aiFeatures.generateRecommendations(
                httpRequestResponse.request().url(),
                result.findings
            );
            output.append("\n").append(recommendations);

            // Rate risk
            int riskLevel = aiFeatures.rateRiskLevel(responseText);
            output.append("Risk Level: ").append(riskLevel).append("/10\n");

            return output.toString();
        }
        catch (Exception e)
        {
            return "Error analyzing traffic: " + e.getMessage();
        }
    }

    /**
     * Determine message received action based on AI analysis
     * 
     * @param requestBody The HTTP request body
     * @param responseBody The HTTP response body
     * @param url The request URL
     * @return MessageReceivedAction enum value
     */
    public static MessageReceivedAction decideRequestAction(String requestBody, String url)
    {
        try
        {
            // Quick pattern check
            if (containsSuspiciousPatterns(requestBody))
            {
                return MessageReceivedAction.INTERCEPT;
            }

            // AI analysis for more complex decisions
            JsonObject analysisData = new JsonObject();
            analysisData.addProperty("url", url);
            analysisData.addProperty("body", requestBody);
            analysisData.addProperty("type", "request");

            String aiAnalysis = communicationBridge.analyzeWithAgent(analysisData);
            
            if (aiAnalysis != null)
            {
                if (aiAnalysis.contains("DROP"))
                {
                    return MessageReceivedAction.DROP;
                }
                if (aiAnalysis.contains("INTERCEPT"))
                {
                    return MessageReceivedAction.INTERCEPT;
                }
                if (aiAnalysis.contains("DO_NOT_INTERCEPT"))
                {
                    return MessageReceivedAction.DO_NOT_INTERCEPT;
                }
            }

            return MessageReceivedAction.CONTINUE;
        }
        catch (Exception e)
        {
            return MessageReceivedAction.CONTINUE;
        }
    }

    /**
     * Determine message received action based on response analysis
     * 
     * @param responseBody The HTTP response body
     * @param statusCode The HTTP status code
     * @param url The request URL
     * @return MessageReceivedAction enum value
     */
    public static MessageReceivedAction decideResponseAction(String responseBody, int statusCode, String url)
    {
        try
        {
            // Quick check for security indicators
            if (statusCode >= 400 || containsSecurityIndicators(responseBody))
            {
                return MessageReceivedAction.INTERCEPT;
            }

            // AI analysis for detailed evaluation
            JsonObject analysisData = new JsonObject();
            analysisData.addProperty("url", url);
            analysisData.addProperty("statusCode", statusCode);
            analysisData.addProperty("body", responseBody);
            analysisData.addProperty("type", "response");

            String aiAnalysis = communicationBridge.analyzeWithAgent(analysisData);
            
            if (aiAnalysis != null)
            {
                if (aiAnalysis.contains("DROP"))
                {
                    return MessageReceivedAction.DROP;
                }
                if (aiAnalysis.contains("INTERCEPT"))
                {
                    return MessageReceivedAction.INTERCEPT;
                }
                if (aiAnalysis.contains("DO_NOT_INTERCEPT"))
                {
                    return MessageReceivedAction.DO_NOT_INTERCEPT;
                }
            }

            return MessageReceivedAction.CONTINUE;
        }
        catch (Exception e)
        {
            return MessageReceivedAction.CONTINUE;
        }
    }

    /**
     * Determine message sent action for outgoing requests
     * 
     * @param requestBody The HTTP request body
     * @param url The request URL
     * @return MessageToBeSentAction enum value
     */
    public static MessageToBeSentAction decideOutgoingRequestAction(String requestBody, String url)
    {
        try
        {
            // Check for dangerous patterns
            if (containsBlockedPatterns(requestBody))
            {
                return MessageToBeSentAction.DROP;
            }

            // AI analysis for decision-making
            JsonObject analysisData = new JsonObject();
            analysisData.addProperty("url", url);
            analysisData.addProperty("body", requestBody);
            analysisData.addProperty("type", "outgoing_request");

            String aiAnalysis = communicationBridge.analyzeWithAgent(analysisData);
            
            if (aiAnalysis != null && aiAnalysis.contains("DROP"))
            {
                return MessageToBeSentAction.DROP;
            }

            return MessageToBeSentAction.CONTINUE;
        }
        catch (Exception e)
        {
            return MessageToBeSentAction.CONTINUE;
        }
    }

    /**
     * Determine message sent action for outgoing responses
     * 
     * @param responseBody The HTTP response body
     * @param statusCode The HTTP status code
     * @return MessageToBeSentAction enum value
     */
    public static MessageToBeSentAction decideOutgoingResponseAction(String responseBody, int statusCode)
    {
        try
        {
            // Check for dangerous patterns
            if (containsBlockedPatterns(responseBody))
            {
                return MessageToBeSentAction.DROP;
            }

            // AI analysis for decision-making
            JsonObject analysisData = new JsonObject();
            analysisData.addProperty("statusCode", statusCode);
            analysisData.addProperty("body", responseBody);
            analysisData.addProperty("type", "outgoing_response");

            String aiAnalysis = communicationBridge.analyzeWithAgent(analysisData);
            
            if (aiAnalysis != null && aiAnalysis.contains("DROP"))
            {
                return MessageToBeSentAction.DROP;
            }

            return MessageToBeSentAction.CONTINUE;
        }
        catch (Exception e)
        {
            return MessageToBeSentAction.CONTINUE;
        }
    }

    /**
     * Check if response contains potential security issues
     */
    public static boolean hasPotentialIssues(HttpHandlerRequestResponse interaction)
    {
        try
        {
            if (interaction.requestResponse() == null || interaction.requestResponse().response() == null)
            {
                return false;
            }

            String responseBody = interaction.requestResponse().response().bodyToString();
            int statusCode = interaction.requestResponse().response().statusCode();

            // Check for common security indicators
            return statusCode >= 400 ||
                   responseBody.toLowerCase().contains("error") ||
                   responseBody.toLowerCase().contains("exception") ||
                   responseBody.toLowerCase().contains("sql") ||
                   responseBody.toLowerCase().contains("xss");
        }
        catch (Exception e)
        {
            return false;
        }
    }

    /**
     * Check for common SQL injection, XSS, and other attack patterns
     */
    private static boolean containsSuspiciousPatterns(String data)
    {
        if (data == null || data.isEmpty())
        {
            return false;
        }

        String lowerData = data.toLowerCase();
        return lowerData.contains("union select") ||
               lowerData.contains("'; drop") ||
               lowerData.contains("<script") ||
               lowerData.contains("onerror=") ||
               lowerData.contains("onclick=") ||
               lowerData.contains("javascript:") ||
               lowerData.contains("../../../") ||
               lowerData.contains("%2e%2e");
    }

    /**
     * Check for security-related indicators in responses
     */
    private static boolean containsSecurityIndicators(String data)
    {
        if (data == null || data.isEmpty())
        {
            return false;
        }

        String lowerData = data.toLowerCase();
        return lowerData.contains("error") ||
               lowerData.contains("exception") ||
               lowerData.contains("sql") ||
               lowerData.contains("unauthorized") ||
               lowerData.contains("forbidden") ||
               lowerData.contains("stack trace");
    }

    /**
     * Check for patterns that should block outgoing messages
     */
    private static boolean containsBlockedPatterns(String data)
    {
        if (data == null || data.isEmpty())
        {
            return false;
        }

        String lowerData = data.toLowerCase();
        return lowerData.contains("delete") ||
               lowerData.contains("drop table") ||
               lowerData.contains("truncate") ||
               lowerData.contains("exec xp_") ||
               lowerData.contains("cmd.exe");
    }
}
}
