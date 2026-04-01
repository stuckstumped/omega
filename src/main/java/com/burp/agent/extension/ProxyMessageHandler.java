/*
 * Copyright (c) 2024. Burp AI Agent Extension
 * 
 * Handles HTTP request interception with AI-driven decision making
 */

package com.burp.agent.extension;

import burp.api.montoya.MontoyaApi;
import burp.api.montoya.proxy.http.InterceptedHttpMessage;
import com.burp.agent.extension.api.MessageReceivedAction;
import com.burp.agent.extension.api.ProxyRequestHandler;
import com.burp.agent.extension.features.AiFeatures;
import com.burp.agent.extension.features.AiFeaturesImpl;
import com.google.gson.Gson;
import com.google.gson.JsonObject;

/**
 * Handles HTTP request interception with AI analysis
 * Determines whether requests should be intercepted, passed through, or dropped
 */
public class ProxyMessageHandler implements ProxyRequestHandler
{
    private final MontoyaApi api;
    private final AiFeatures aiFeatures;
    private final AgentCommunicationBridge communicationBridge;
    private static final Gson gson = new Gson();

    public ProxyMessageHandler(MontoyaApi api)
    {
        this.api = api;
        this.aiFeatures = new AiFeaturesImpl();
        this.communicationBridge = new AgentCommunicationBridge();
    }

    @Override
    public MessageReceivedAction handleRequest(InterceptedHttpMessage message)
    {
        try
        {
            String requestBody = message.request().bodyToString();
            String requestUrl = message.request().url();

            // First pass: Quick pattern-based analysis
            if (containsSuspiciousPatterns(requestBody))
            {
                api.logging().logToOutput("[AI Agent] Suspicious request pattern detected: " + requestUrl);
                return MessageReceivedAction.INTERCEPT;
            }

            // Second pass: AI-based analysis via agent service
            JsonObject analysisData = new JsonObject();
            analysisData.addProperty("url", requestUrl);
            analysisData.addProperty("method", message.request().method());
            analysisData.addProperty("body", requestBody);
            analysisData.addProperty("type", "request");

            String aiAnalysis = communicationBridge.analyzeWithAgent(analysisData);

            if (aiAnalysis != null && aiAnalysis.contains("INTERCEPT"))
            {
                api.logging().logToOutput("[AI Agent] Request flagged for review: " + requestUrl);
                return MessageReceivedAction.INTERCEPT;
            }

            if (aiAnalysis != null && aiAnalysis.contains("DROP"))
            {
                api.logging().logToOutput("[AI Agent] Dropping request: " + requestUrl);
                return MessageReceivedAction.DROP;
            }

            // Default: proceed with current interception rules
            return MessageReceivedAction.CONTINUE;
        }
        catch (Exception e)
        {
            api.logging().logToError("Error handling request: " + e.getMessage());
            return MessageReceivedAction.CONTINUE;
        }
    }

    /**
     * Check for common SQL injection, XSS, and other attack patterns
     */
    private boolean containsSuspiciousPatterns(String data)
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
}
