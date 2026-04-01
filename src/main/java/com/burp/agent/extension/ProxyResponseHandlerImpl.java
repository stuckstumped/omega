/*
 * Copyright (c) 2024. Burp AI Agent Extension
 * 
 * Handles HTTP response interception with AI-driven decision making
 */

package com.burp.agent.extension;

import burp.api.montoya.MontoyaApi;
import burp.api.montoya.proxy.http.InterceptedHttpMessage;
import com.burp.agent.extension.api.MessageReceivedAction;
import com.burp.agent.extension.api.ProxyResponseHandler;
import com.google.gson.JsonObject;

/**
 * Handles HTTP response interception with AI analysis
 * Determines whether responses should be intercepted, passed through, or dropped
 */
public class ProxyResponseHandlerImpl implements ProxyResponseHandler
{
    private final MontoyaApi api;
    private final AgentCommunicationBridge communicationBridge;

    public ProxyResponseHandlerImpl(MontoyaApi api)
    {
        this.api = api;
        this.communicationBridge = new AgentCommunicationBridge();
    }

    @Override
    public MessageReceivedAction handleResponse(InterceptedHttpMessage message)
    {
        try
        {
            String responseBody = message.response() != null ? 
                                 message.response().bodyToString() : "";
            int statusCode = message.response() != null ? 
                            message.response().statusCode() : 0;
            String requestUrl = message.request().url();

            // First pass: Check for common security indicators
            if (statusCode >= 400 || containsSecurityIndicators(responseBody))
            {
                api.logging().logToOutput("[AI Agent] Security indicator detected in response: " + requestUrl);
                return MessageReceivedAction.INTERCEPT;
            }

            // Second pass: AI-based analysis via agent service
            JsonObject analysisData = new JsonObject();
            analysisData.addProperty("url", requestUrl);
            analysisData.addProperty("statusCode", statusCode);
            analysisData.addProperty("body", responseBody);
            analysisData.addProperty("type", "response");

            String aiAnalysis = communicationBridge.analyzeWithAgent(analysisData);

            if (aiAnalysis != null && aiAnalysis.contains("INTERCEPT"))
            {
                api.logging().logToOutput("[AI Agent] Response flagged for review: " + requestUrl);
                return MessageReceivedAction.INTERCEPT;
            }

            if (aiAnalysis != null && aiAnalysis.contains("DROP"))
            {
                api.logging().logToOutput("[AI Agent] Dropping response: " + requestUrl);
                return MessageReceivedAction.DROP;
            }

            // Default: proceed with current interception rules
            return MessageReceivedAction.CONTINUE;
        }
        catch (Exception e)
        {
            api.logging().logToError("Error handling response: " + e.getMessage());
            return MessageReceivedAction.CONTINUE;
        }
    }

    /**
     * Check for security-related indicators in responses
     */
    private boolean containsSecurityIndicators(String data)
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
}
