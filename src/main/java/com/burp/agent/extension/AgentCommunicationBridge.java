/*
 * Copyright (c) 2024. Burp AI Agent Extension
 * 
 * Agent communicator for sending traffic analysis requests to the Python AI agent
 */

package com.burp.agent.extension;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import org.apache.hc.client5.http.classic.methods.HttpPost;
import org.apache.hc.client5.http.impl.classic.CloseableHttpClient;
import org.apache.hc.client5.http.impl.classic.HttpClients;
import org.apache.hc.core5.http.ContentType;
import org.apache.hc.core5.http.io.entity.StringEntity;

import java.nio.charset.StandardCharsets;

/**
 * Communicates with the Python AI Agent via HTTP
 */
public class AgentCommunicationBridge
{
    private static final String AGENT_HOST = "localhost";
    private static final int AGENT_PORT = Integer.parseInt(System.getenv().getOrDefault("AGENT_PORT", "9999"));
    private static final String ANALYZE_ENDPOINT = "/analyze";
    private static final Gson gson = new Gson();

    /**
     * Send request/response data to Python agent for analysis
     * 
     * @param requestData JSON data containing request/response details
     * @return Analysis result from the agent
     */
    public static String analyzeWithAgent(JsonObject requestData)
    {
        try (CloseableHttpClient client = HttpClients.createDefault())
        {
            String url = String.format("http://%s:%d%s", AGENT_HOST, AGENT_PORT, ANALYZE_ENDPOINT);
            HttpPost request = new HttpPost(url);
            
            String jsonBody = gson.toJson(requestData);
            request.setEntity(new StringEntity(jsonBody, ContentType.APPLICATION_JSON));
            request.setHeader("Content-Type", "application/json");
            
            return client.execute(request, response -> {
                if (response.getCode() == 200)
                {
                    return response.getEntity().toString();
                }
                return null;
            });
        }
        catch (Exception e)
        {
            return "Error communicating with agent: " + e.getMessage();
        }
    }

    /**
     * Send scan request to agent
     */
    public static String requestScan(String url, String scanType)
    {
        JsonObject request = new JsonObject();
        request.addProperty("action", "scan");
        request.addProperty("url", url);
        request.addProperty("type", scanType);
        return analyzeWithAgent(request);
    }

    /**
     * Send spider request to agent
     */
    public static String requestSpider(String url)
    {
        JsonObject request = new JsonObject();
        request.addProperty("action", "spider");
        request.addProperty("url", url);
        return analyzeWithAgent(request);
    }

    /**
     * Request issue analysis from agent
     */
    public static String requestIssueAnalysis(String requestData, String responseData)
    {
        JsonObject request = new JsonObject();
        request.addProperty("action", "analyze_traffic");
        request.addProperty("request", requestData);
        request.addProperty("response", responseData);
        return analyzeWithAgent(request);
    }
}
