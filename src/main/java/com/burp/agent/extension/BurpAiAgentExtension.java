/*
 * Copyright (c) 2022-2023. PortSwigger Ltd. All rights reserved.
 *
 * This code may be used to extend the functionality of Burp Suite Community Edition
 * and Burp Suite Professional, provided that this usage does not violate the
 * license terms for those products.
 */

package com.burp.agent.extension;

import burp.api.montoya.BurpExtension;
import burp.api.montoya.MontoyaApi;
import burp.api.montoya.extension.ExtensionUnloadingHandler;
import burp.api.montoya.http.handler.HttpHandler;
import burp.api.montoya.http.handler.HttpHandlerRequestResponse;
import burp.api.montoya.http.message.responses.HttpResponse;
import com.burp.agent.extension.api.EnhancedCapability;

import java.util.Set;
import java.util.HashSet;

/**
 * Burp Suite Extension for AI Agent Integration
 * 
 * This extension integrates the Python AI agent with Burp Suite,
 * allowing the agent to intercept, analyze, and modify HTTP traffic
 * in real-time.
 */
public class BurpAiAgentExtension implements BurpExtension
{
    private MontoyaApi api;
    private static final String EXTENSION_NAME = "Burp AI Agent";
    private static final String EXTENSION_VERSION = "1.0.0";

    @Override
    public void initialize(MontoyaApi api)
    {
        this.api = api;
        
        // Log extension initialization
        api.logging().logToOutput("Initializing " + EXTENSION_NAME + " v" + EXTENSION_VERSION);
        
        // Register HTTP handler for request/response interception
        api.http().registerHttpHandler(new AiAgentHttpHandler(api));
        
        // Register proxy request and response handlers with AI decision-making
        api.proxy().registerRequestHandler(new ProxyMessageHandler(api));
        api.proxy().registerResponseHandler(new ProxyResponseHandlerImpl(api));
        
        // Register extension unload handler
        api.extension().registerExtensionUnloadingHandler(this::onExtensionUnload);
        
        api.logging().logToOutput(EXTENSION_NAME + " proxy handlers registered with AI analysis enabled");
        api.logging().logToOutput(EXTENSION_NAME + " successfully initialized");
    }

    @Override
    public Set<EnhancedCapability> enhancedCapabilities()
    {
        Set<EnhancedCapability> capabilities = new HashSet<>();
        capabilities.add(EnhancedCapability.AI_FEATURES);
        api.logging().logToOutput("Requesting enhanced AI capabilities");
        return capabilities;
    }

    /**
     * Handle extension unloading
     */
    private void onExtensionUnload()
    {
        api.logging().logToOutput(EXTENSION_NAME + " unloading");
    }

    /**
     * HTTP Handler for intercepting and analyzing requests/responses
     */
    private static class AiAgentHttpHandler implements HttpHandler
    {
        private final MontoyaApi api;
        private final AgentCommunicator communicator;

        public AiAgentHttpHandler(MontoyaApi api)
        {
            this.api = api;
            this.communicator = new AgentCommunicator();
        }

        @Override
        public void handleHttpRequestResponse(HttpHandlerRequestResponse interaction)
        {
            try
            {
                // Send request/response data to Python agent for analysis
                String analysisResult = communicator.analyzeTraffic(interaction);
                
                if (analysisResult != null && !analysisResult.isEmpty())
                {
                    api.logging().logToOutput("[AI Agent] " + analysisResult);
                }
            }
            catch (Exception e)
            {
                api.logging().logToError("Error in AI Agent HTTP handler: " + e.getMessage());
            }
        }
    }

    /**
     * Communicator for sending data to the Python AI Agent
     */
    private static class AgentCommunicator
    {
        private static final String AGENT_HOST = "localhost";
        private static final int AGENT_PORT = 9999;

        public String analyzeTraffic(HttpHandlerRequestResponse interaction)
        {
            // This would communicate with the Python agent
            // For now, returning a placeholder
            return "Traffic analyzed by AI Agent";
        }
    }
}
