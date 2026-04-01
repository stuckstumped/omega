/*
 * Copyright (c) 2024. Burp AI Agent Extension
 * 
 * Handles proxy messages being sent with AI-driven decision making
 */

package com.burp.agent.extension;

import burp.api.montoya.MontoyaApi;
import burp.api.montoya.proxy.http.InterceptedHttpMessage;
import burp.api.montoya.proxy.http.ProxyMessageSentHandler;
import com.burp.agent.extension.api.MessageToBeSentAction;
import com.google.gson.JsonObject;

/**
 * Handles outgoing HTTP proxy messages with AI analysis
 * Determines whether messages should be forwarded or dropped
 */
public class ProxyMessageSentHandler implements ProxyMessageSentHandler
{
    private final MontoyaApi api;
    private final AgentCommunicationBridge communicationBridge;

    public ProxyMessageSentHandler(MontoyaApi api)
    {
        this.api = api;
        this.communicationBridge = new AgentCommunicationBridge();
    }

    @Override
    public MessageToBeSentAction handleRequestSent(InterceptedHttpMessage message)
    {
        try
        {
            String requestBody = message.request().bodyToString();
            String requestUrl = message.request().url();

            // Check for blocking patterns
            if (containsBlockedPatterns(requestBody))
            {
                api.logging().logToOutput("[AI Agent] Blocking outgoing request: " + requestUrl);
                return MessageToBeSentAction.DROP;
            }

            // AI-based analysis for outgoing requests
            JsonObject analysisData = new JsonObject();
            analysisData.addProperty("url", requestUrl);
            analysisData.addProperty("method", message.request().method());
            analysisData.addProperty("body", requestBody);
            analysisData.addProperty("type", "request_sent");

            String aiAnalysis = communicationBridge.analyzeWithAgent(analysisData);

            if (aiAnalysis != null && aiAnalysis.contains("DROP"))
            {
                api.logging().logToOutput("[AI Agent] Dropping outgoing request: " + requestUrl);
                return MessageToBeSentAction.DROP;
            }

            // Default: forward message
            return MessageToBeSentAction.CONTINUE;
        }
        catch (Exception e)
        {
            api.logging().logToError("Error handling outgoing request: " + e.getMessage());
            return MessageToBeSentAction.CONTINUE;
        }
    }

    @Override
    public MessageToBeSentAction handleResponseSent(InterceptedHttpMessage message)
    {
        try
        {
            String responseBody = message.response() != null ? 
                                 message.response().bodyToString() : "";
            int statusCode = message.response() != null ? 
                            message.response().statusCode() : 0;

            // Check for blocking patterns
            if (containsBlockedPatterns(responseBody))
            {
                api.logging().logToOutput("[AI Agent] Blocking outgoing response with status: " + statusCode);
                return MessageToBeSentAction.DROP;
            }

            // AI-based analysis for outgoing responses
            JsonObject analysisData = new JsonObject();
            analysisData.addProperty("statusCode", statusCode);
            analysisData.addProperty("body", responseBody);
            analysisData.addProperty("type", "response_sent");

            String aiAnalysis = communicationBridge.analyzeWithAgent(analysisData);

            if (aiAnalysis != null && aiAnalysis.contains("DROP"))
            {
                api.logging().logToOutput("[AI Agent] Dropping outgoing response");
                return MessageToBeSentAction.DROP;
            }

            // Default: forward message
            return MessageToBeSentAction.CONTINUE;
        }
        catch (Exception e)
        {
            api.logging().logToError("Error handling outgoing response: " + e.getMessage());
            return MessageToBeSentAction.CONTINUE;
        }
    }

    /**
     * Check for patterns that should block outgoing messages
     */
    private boolean containsBlockedPatterns(String data)
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
