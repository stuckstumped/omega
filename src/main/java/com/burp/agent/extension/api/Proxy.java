/*
 * Copyright (c) 2022-2023. PortSwigger Ltd. All rights reserved.
 *
 * This code may be used to extend the functionality of Burp Suite Community Edition
 * and Burp Suite Professional, provided that this usage does not violate the
 * license terms for those products.
 */

package com.burp.agent.extension.api;

import burp.api.montoya.core.Registration;
import java.util.List;

/**
 * Provides access to the functionality of the Proxy tool.
 */
public interface Proxy
{
    /**
     * Register a handler which will be notified of requests being processed by the Proxy tool.
     */
    Registration registerRequestHandler(ProxyRequestHandler handler);

    /**
     * Register a handler which will be notified of responses being processed by the Proxy tool.
     */
    Registration registerResponseHandler(ProxyResponseHandler handler);

    /**
     * Enable master interception for Burp Proxy.
     */
    void enableIntercept();

    /**
     * Disable master interception for Burp Proxy.
     */
    void disableIntercept();

    /**
     * Check if master interception is enabled.
     */
    boolean isInterceptEnabled();
}
