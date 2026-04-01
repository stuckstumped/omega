# Burp Suite AI Agent Extension - Proxy Message Integration

## Summary

Successfully integrated the foundational Burp Suite Montoya API proxy message handling enums into the AI Agent extension with complete implementation of handler classes and AI-driven decision-making logic.

## Files Created

### 1. **API Enum Definitions**

#### MessageReceivedAction.java
- Defines actions for initially received proxy messages
- Values: `CONTINUE`, `INTERCEPT`, `DO_NOT_INTERCEPT`, `DROP`
- Location: `src/main/java/com/burp/agent/extension/api/`
- Used by: ProxyMessageHandler for incoming requests/responses

#### MessageToBeSentAction.java
- Defines actions for messages being sent through proxy
- Values: `CONTINUE`, `DROP`
- Location: `src/main/java/com/burp/agent/extension/api/`
- Used by: ProxyMessageSentHandler for outgoing traffic

### 2. **Message Handler Implementations**

#### ProxyMessageHandler.java
- Implements Burp Suite's ProxyMessageHandler interface
- **Features:**
  - `handleRequestReceived()` - Analyzes incoming requests with AI
  - `handleResponseReceived()` - Analyzes incoming responses with AI
  - Two-pass analysis: Pattern-based + AI-based decision making
  - Returns appropriate MessageReceivedAction enum values
  - Integrates with AgentCommunicationBridge for AI analysis
  - Pattern detection for SQL injection, XSS, path traversal attacks
  - Security indicator detection in responses

#### ProxyMessageSentHandler.java
- Implements ProxyMessageSentHandler interface for outgoing traffic
- **Features:**
  - `handleRequestSent()` - Analyzes outgoing requests
  - `handleResponseSent()` - Analyzes outgoing responses
  - Returns MessageToBeSentAction values (CONTINUE or DROP)
  - Blocks dangerous patterns before sending
  - AI-based analysis for complex threats

### 3. **Enhanced TrafficAnalyzer.java**

**New Methods:**
- `decideRequestAction()` - Uses MessageReceivedAction enum
- `decideResponseAction()` - Uses MessageReceivedAction enum
- `decideOutgoingRequestAction()` - Uses MessageToBeSentAction enum
- `decideOutgoingResponseAction()` - Uses MessageToBeSentAction enum

**Pattern Detection Methods:**
- `containsSuspiciousPatterns()` - Detects injection and XSS attempts
- `containsSecurityIndicators()` - Detects error pages and stack traces
- `containsBlockedPatterns()` - Detects dangerous SQL and system commands

### 4. **Updated BurpAiAgentExtension.java**

**Handler Registration:**
```java
api.proxy().registerRequestHandler(new ProxyMessageHandler(api));
api.proxy().registerResponseHandler(new ProxyMessageHandler(api));
api.proxy().registerMessageSentHandler(new ProxyMessageSentHandler(api));
```

## Architecture Flow

### Incoming Message (Request/Response)
```
Burp Proxy → ProxyMessageHandler
             ├─ Pattern Check (SQL injection, XSS, etc.)
             ├─ Return INTERCEPT (if suspicious)
             └─ AI Analysis via AgentCommunicationBridge
                ├─ INTERCEPT → User review
                ├─ DROP → Block message
                ├─ DO_NOT_INTERCEPT → Auto-forward
                └─ CONTINUE → Follow rules
```

### Outgoing Message (Request/Response)
```
Burp Proxy → ProxyMessageSentHandler
             ├─ Pattern Check (DROP if dangerous)
             └─ AI Analysis via AgentCommunicationBridge
                ├─ DROP → Block message
                └─ CONTINUE → Forward message
```

## Key Features

1. **Dual-Mode Analysis:**
   - Quick pattern-based detection for known threats
   - AI-powered analysis for complex/novel threats

2. **Flexible Decision Making:**
   - Four distinct actions for received messages
   - Two distinct actions for sent messages
   - Configurable based on AI analysis results

3. **Security Pattern Detection:**
   - SQL injection patterns: `UNION SELECT`, `'; DROP`
   - XSS patterns: `<script>`, event handlers, `javascript:`
   - Path traversal: `../../../`, `%2e%2e`
   - Dangerous database/system commands

4. **Logging & Monitoring:**
   - All decisions logged to Burp output
   - Detailed reasoning for INTERCEPT/DROP actions
   - Integration with Burp's native logging

5. **Scalable Architecture:**
   - Separate handlers for requests/responses
   - Separates incoming vs outgoing traffic logic
   - Ready for Ollama/HuggingFace AI model integration

## Integration Points

- **AgentCommunicationBridge:** Sends analysis data to Python AI agent
- **AiFeatures/AiFeaturesImpl:** Pattern-based analysis and risk rating
- **MontoyaApi:** Registers handlers, logs events
- **Configuration System:** Ready for model selection (Ollama/HuggingFace)

## Next Steps (Future Enhancement)

1. Implement custom system prompt storage
2. Add model backend selection UI (Ollama vs HuggingFace)
3. Persist configuration preferences
4. Add performance metrics and decision analytics
5. Implement decision feedback loop for model training

## Compilation Status

✅ All files compile without errors
✅ No missing dependencies
✅ Proper enum usage throughout
✅ Type-safe decision flow

## Testing Recommendations

1. Test with benign HTTP traffic (should return CONTINUE)
2. Test with SQL injection payloads (should return INTERCEPT)
3. Test with XSS payloads (should return INTERCEPT)
4. Verify logging output captures all decisions
5. Test handler registration in Burp Suite
