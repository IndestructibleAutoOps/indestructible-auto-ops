#!/bin/bash

# GL Governance Markers
# @gl-layer GL-00-NAMESPACE
# @gl-module ns-root/namespaces-sdk
# @gl-semantic-anchor GL-00-NAMESPAC_FIXTYPESCRIP
# @gl-evidence-required false
# GL Unified Charter Activated

# Fix TypeScript Build Errors - Critical Fixes First

set -e

cd "$(dirname "$0")"

echo "🔧 Fixing TypeScript Build Errors - Phase 1: Critical Dependencies"
echo "================================================================"

# Phase 1: Install critical missing dependencies
echo ""
echo "📦 Phase 1: Installing Missing Dependencies"
echo "------------------------------------------"

echo "Installing @types/node..."
npm install --save-dev @types/node

echo "Installing commander and @types/commander..."
npm install commander
npm install --save-dev @types/commander

echo "Installing tslib..."
npm install tslib

echo ""
echo "✅ Phase 1 Complete: Dependencies installed"
echo ""

# Phase 2: Update tsconfig.json
echo "📝 Phase 2: Updating tsconfig.json"
echo "----------------------------------"

# Backup original tsconfig.json
cp tsconfig.json tsconfig.json.backup

# Create updated tsconfig.json
cat > tsconfig.json << 'EOF'
{
  "compilerOptions": {
    /* Language and Environment */
    "target": "ES2020",
    "lib": ["ES2020", "DOM"],
    
    /* Modules */
    "module": "commonjs",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    
    /* Emit */
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist",
    "removeComments": true,
    "importHelpers": true,
    
    /* Interop Constraints */
    "isolatedModules": true,
    "forceConsistentCasingInFileNames": true,
    
    /* Type Checking */
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true,
    "noUnusedLocals": false,
    "noUnusedParameters": false,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": false,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": false,
    
    /* Completeness */
    "skipLibCheck": true,
    "types": ["node"]
  },
  "include": [
    "src/**/*"
  ],
  "exclude": [
    "node_modules",
    "dist",
    "**/*.test.ts",
    "**/*.spec.ts"
  ]
}
EOF

echo "✅ tsconfig.json updated"
echo ""

# Phase 3: Try building
echo "🏗️  Phase 3: Attempting Build"
echo "------------------------------"

npm run build || {
    echo ""
    echo "⚠️  Build still has errors, but critical issues are fixed"
    echo "   See remaining errors in output above"
    exit 1
}

echo ""
echo "✅ Build Successful!"
echo ""
echo "📊 Summary:"
echo "   - Installed @types/node"
echo "   - Installed commander and @types/commander"
echo "   - Installed tslib"
echo "   - Updated tsconfig.json"
echo ""
echo "🎉 TypeScript compilation successful!"