/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-mcp/level4/tests
 * @gl-semantic-anchor GL-00-LEVEL4_TESTS_SETUP
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * Jest Test Setup
 */

process.env.NODE_ENV = 'test';

global.console = {
  ...console,
  log: jest.fn(),
  debug: jest.fn(),
  info: jest.fn(),
  warn: jest.fn(),
  error: jest.fn(),
};

jest.setTimeout(10000);

afterEach(() => {
  jest.clearAllMocks();
});