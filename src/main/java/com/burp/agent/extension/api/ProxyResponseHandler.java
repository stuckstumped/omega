/*
 * Copyright (c) 2022-2023. PortSwigger Ltd. All rights reserved.
 *
 * This code may be used to extend the functionality of Burp Suite Community Edition
 * and Burp Suite Professional, provided that this usage does not violate the
 * license terms for those products.
 */

package com.burp.agent.extension.api;

import burp.api.montoya.proxy.http.InterceptedHttpMessage;

/**
 * Handlers of this type can be registered with the Proxy tool to perform
 * custom analysis and modification of HTTP responses. Handlers will be notified
 * of responses being processed by the Proxy tool, and have the option to modify
 * the response or control in-UI message interception.
 */
public interface ProxyResponseHandler
{
    /**
     * This method is invoked when an HTTP response is received by the Proxy tool.
     *
     * @param message The HTTP response that was received.
     *
     * @return The {@link MessageReceivedAction} that should be taken for the response.
     */
    MessageReceivedAction handleResponse(InterceptedHttpMessage message);
}
