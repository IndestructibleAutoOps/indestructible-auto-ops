# GL Unified Charter Activated
# Extended Platforms Integration Guide

## Overview

This guide provides comprehensive instructions for integrating MachineNativeOps with Cloudflare, Supabase, GitBook, and additional third-party platforms.

---

## Supported Platforms

### Cloudflare
- ✅ Cloudflare Workers (Edge computing)
- ✅ Cloudflare Pages (Static sites)
- ✅ Cloudflare D1 (SQLite database)
- ✅ Cloudflare KV (Key-value storage)
- ✅ Cloudflare R2 (S3-compatible storage)
- ✅ Cloudflare Durable Objects (Stateful storage)
- ✅ Cloudflare Access (Zero Trust)
- ✅ Cloudflare Email Routing

### Supabase
- ✅ PostgreSQL Database
- ✅ Authentication (Email, OAuth, MFA)
- ✅ Storage (Files, images, backups)
- ✅ Edge Functions (Serverless)
- ✅ Realtime (WebSockets)
- ✅ Row Level Security

### GitBook
- ✅ Documentation platform
- ✅ API Reference
- ✅ Code samples
- ✅ Interactive components
- ✅ SEO optimization
- ✅ Analytics integration

### Additional Platforms
- ✅ Vercel (Frontend deployment)
- ✅ Netlify (Frontend deployment)
- ✅ Render (Backend deployment)
- ✅ Railway (Full-stack deployment)

---

## Cloudflare Integration

### Prerequisites
```bash
# Install Wrangler CLI
npm install -g wrangler

# Authenticate
wrangler login
```

### Environment Variables
```bash
export CLOUDFLARE_ENABLED=true
export CLOUDFLARE_API_TOKEN=your_api_token
export CLOUDFLARE_ACCOUNT_ID=your_account_id
export CLOUDFLARE_ZONE_ID=your_zone_id
export CLOUDFLARE_WORKER_NAME=machine-native-ops-worker
export CLOUDFLARE_KV_NAMESPACE_ID=your_kv_namespace_id
export CLOUDFLARE_R2_BUCKET=machine-native-ops
export CLOUDFLARE_D1_DATABASE_ID=your_d1_database_id
```

### Cloudflare Workers Deployment
```bash
# 1. Create worker
wrangler init machine-native-ops-worker

# 2. Add bindings to wrangler.toml
cat > wrangler.toml << EOF
name = "machine-native-ops-worker"
main = "src/index.ts"
compatibility_date = "2024-01-01"

[[kv_namespaces]]
binding = "KV_NAMESPACE"
id = "${CLOUDFLARE_KV_NAMESPACE_ID}"

[[r2_buckets]]
binding = "R2_BUCKET"
bucket_name = "machine-native-ops"

[[d1_databases]]
binding = "D1_DATABASE"
database_name = "machine-native-ops-db"
database_id = "${CLOUDFLARE_D1_DATABASE_ID}"

[durable_objects]
bindings = [
  { name = "DURABLE_OBJECT", class_name = "MachineNativeOpsObject" }
]

[vars]
ENVIRONMENT = "production"
LOG_LEVEL = "info"
DATABASE_URL = "${DATABASE_URL}"
REDIS_URL = "${REDIS_URL}"

[triggers]
crons = ["0 * * * *"]  # Every hour
EOF

# 3. Deploy worker
wrangler deploy

# 4. Test worker
curl https://machine-native-ops-worker.your-subdomain.workers.dev
```

### Cloudflare Pages Deployment
```bash
# 1. Create Pages project
wrangler pages project create machine-native-ops-docs

# 2. Deploy to Pages
wrangler pages deploy ./dist --project-name=machine-native-ops-docs

# 3. Configure custom domain
wrangler pages domain create docs.machine-native-ops.com --project-name=machine-native-ops-docs
```

### Cloudflare D1 Setup
```bash
# 1. Create D1 database
wrangler d1 create machine-native-ops-db

# 2. Get database ID
export CLOUDFLARE_D1_DATABASE_ID=<output_from_previous_command>

# 3. Run migrations
wrangler d1 execute machine-native-ops-db --file=./migrations/001_init.sql

# 4. Query database
wrangler d1 execute machine-native-ops-db --command="SELECT * FROM users"
```

### Cloudflare R2 Setup
```bash
# 1. Create R2 bucket
wrangler r2 bucket create machine-native-ops

# 2. Upload files
wrangler r2 object put machine-native-ops/file.txt --file=./file.txt

# 3. List objects
wrangler r2 object list machine-native-ops

# 4. Download files
wrangler r2 object get machine-native-ops/file.txt --file=./downloaded-file.txt
```

---

## Supabase Integration

### Prerequisites
```bash
# Install Supabase CLI
npm install -g supabase

# Initialize Supabase
supabase init
```

### Environment Variables
```bash
export SUPABASE_ENABLED=true
export SUPABASE_PROJECT_ID=your_project_id
export SUPABASE_API_URL=https://your-project-id.supabase.co
export SUPABASE_ANON_KEY=your_anon_key
export SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
export SUPABASE_DATABASE_URL=postgresql://postgres:[PASSWORD]@db.your-project-id.supabase.co:5432/postgres
export SUPABASE_MFA_ENABLED=true
export GOOGLE_AUTH_ENABLED=true
export GITHUB_AUTH_ENABLED=true
```

### Database Setup
```bash
# 1. Link to Supabase project
supabase link --project-ref ${SUPABASE_PROJECT_ID}

# 2. Create migration
supabase migration new init_schema

# 3. Write migration SQL
cat > supabase/migrations/20240127_init_schema.sql << EOF
-- Users table
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email TEXT UNIQUE NOT NULL,
  name TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Profiles table
CREATE TABLE IF NOT EXISTS profiles (
  id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
  avatar_url TEXT,
  bio TEXT,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tasks table
CREATE TABLE IF NOT EXISTS tasks (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  description TEXT,
  status TEXT DEFAULT 'pending',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Row Level Security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY "Users can view own profile" ON users
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON users
  FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can view all profiles" ON profiles
  FOR SELECT USING (true);

CREATE POLICY "Users can update own profile" ON profiles
  FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can view own tasks" ON tasks
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own tasks" ON tasks
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own tasks" ON tasks
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own tasks" ON tasks
  FOR DELETE USING (auth.uid() = user_id);
EOF

# 4. Apply migration
supabase db push

# 5. Generate TypeScript types
supabase gen types typescript --local > src/types/supabase.ts
```

### Storage Setup
```bash
# 1. Create storage buckets
supabase storage create-bucket documents
supabase storage create-bucket images
supabase storage create-bucket backups

# 2. Create storage policies
supabase storage create-policy documents-select-own \
  --bucket=documents \
  --definition="auth.uid() = storage.foldername" \
  --operations=SELECT

supabase storage create-policy documents-insert-own \
  --bucket=documents \
  --definition="auth.uid() = storage.foldername" \
  --operations=INSERT

# 3. Upload file
supabase storage upload --bucket=documents --path=document.txt ./document.txt

# 4. List files
supabase storage list --bucket=documents
```

### Edge Functions Deployment
```bash
# 1. Create edge function
supabase functions new webhook-handler

# 2. Write function code
cat > supabase/functions/webhook-handler/index.ts << 'EOF'
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const supabase = createClient(
  Deno.env.get('SUPABASE_URL') ?? '',
  Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
)

serve(async (req) => {
  try {
    const { method } = req
    
    if (method !== 'POST') {
      return new Response('Method not allowed', { status: 405 })
    }

    const payload = await req.json()
    console.log('Received webhook:', payload)

    // Process webhook
    const { data, error } = await supabase
      .from('webhooks')
      .insert({ payload })
      .select()

    if (error) {
      console.error('Error processing webhook:', error)
      return new Response(JSON.stringify({ error: error.message }), { 
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      })
    }

    return new Response(JSON.stringify({ success: true, data }), {
      headers: { 'Content-Type': 'application/json' }
    })
  } catch (error) {
    console.error('Error:', error)
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    })
  }
})
EOF

# 3. Deploy function
supabase functions deploy webhook-handler

# 4. Test function
curl -X POST https://your-project-id.supabase.co/functions/v1/webhook-handler \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

### Realtime Setup
```bash
# 1. Enable realtime for tables
supabase realtime publish notifications
supabase realtime publish tasks

# 2. Subscribe to realtime events (in your application)
# Example using JavaScript client:
const { createClient } = '@supabase/supabase-js'

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_ANON_KEY
)

// Subscribe to notifications
const notificationsChannel = supabase
  .channel('user-notifications')
  .on('postgres_changes', {
    event: 'INSERT',
    schema: 'public',
    table: 'notifications',
    filter: `user_id=eq.${userId}`
  }, (payload) => {
    console.log('New notification:', payload)
  })
  .subscribe()
```

---

## GitBook Integration

### Prerequisites
```bash
# Install GitBook CLI (if available)
# Or use GitBook web interface

# Install Git (required for GitHub integration)
git --version
```

### Environment Variables
```bash
export GITBOOK_ENABLED=true
export GITBOOK_SPACE_ID=your_space_id
export GITBOOK_ACCESS_TOKEN=your_access_token
export GITBOOK_API_REFERENCE_ENABLED=true
export GITBOOK_ANALYTICS_ENABLED=true
export GITBOOK_GITHUB_INTEGRATION_ENABLED=true
```

### GitBook Space Setup
```bash
# 1. Create GitBook space via web interface
# Go to https://app.gitbook.com and create a new space

# 2. Set up GitHub integration
# In GitBook space settings -> Integrations -> GitHub
# Connect repository: MachineNativeOps/machine-native-ops

# 3. Configure sync settings
# - Sync branches: main, develop
# - Auto-sync: enabled
# - Create pull requests: enabled
```

### Content Structure Setup
```bash
# 1. Create documentation directory structure
mkdir -p docs/{getting-started,guides,tutorials,reference}

# 2. Create navigation file
cat > docs/SUMMARY.md << EOF
# Table of Contents

## Getting Started
- [Introduction](getting-started/introduction.md)
- [Quick Start](getting-started/quick-start.md)
- [Installation](getting-started/installation.md)

## Guides
- [Deployment Guide](guides/deployment.md)
- [Configuration Guide](guides/configuration.md)
- [API Reference](guides/api-reference.md)

## Tutorials
- [Basic Tutorial](tutorials/basic-tutorial.md)
- [Advanced Tutorial](tutorials/advanced-tutorial.md)

## Reference
- [Glossary](reference/glossary.md)
- [FAQ](reference/faq.md)
EOF

# 3. Create documentation files
cat > docs/getting-started/introduction.md << EOF
# Introduction

Welcome to MachineNativeOps documentation.

## What is MachineNativeOps?

MachineNativeOps is a comprehensive platform for...

## Key Features

- Feature 1
- Feature 2
- Feature 3

## Getting Started

Read the [Quick Start](./quick-start.md) guide to get started.
EOF
```

### API Reference Setup
```bash
# 1. Create OpenAPI specification
cat > openapi.yaml << EOF
openapi: 3.0.0
info:
  title: MachineNativeOps API
  version: 1.0.0
  description: MachineNativeOps API Reference

servers:
  - url: https://api.machine-native-ops.com
    description: Production API
  - url: https://staging-api.machine-native-ops.com
    description: Staging API

paths:
  /health:
    get:
      summary: Health check endpoint
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: healthy

  /api/v1/users:
    get:
      summary: List all users
      security:
        - bearerAuth: []
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
        email:
          type: string
          format: email
        name:
          type: string
EOF

# 2. Upload OpenAPI spec to GitBook
# Via GitBook web interface: Settings -> API Reference -> Import from URL or file
```

### Analytics Setup
```bash
# 1. Enable analytics in GitBook
# Via web interface: Settings -> Analytics

# 2. Configure Google Analytics
export GA_TRACKING_ID=G-XXXXXXXXXX

# 3. Configure Plausible Analytics (alternative)
export PLAUSIBLE_ENABLED=true
export PLAUSIBLE_DOMAIN=machine-native-ops.gitbook.io

# 4. Configure Amplitude (alternative)
export AMPLITUDE_ENABLED=true
export AMPLITUDE_API_KEY=your_api_key
```

---

## Additional Platforms

### Vercel Deployment
```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel --prod

# Environment variables
vercel env add DATABASE_URL production
vercel env add REDIS_URL production
```

### Netlify Deployment
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Deploy
netlify deploy --prod

# Environment variables
netlify env:set DATABASE_URL production
netlify env:set REDIS_URL production
```

### Render Deployment
```bash
# Deploy via Render web interface
# Or use Render CLI

# Environment variables
# Set via Render dashboard or CLI
export DATABASE_URL=your_database_url
export REDIS_URL=your_redis_url
```

### Railway Deployment
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up

# Environment variables
railway variables set DATABASE_URL=your_database_url
railway variables set REDIS_URL=your_redis_url
```

---

## Integration Examples

### Full Stack Example (Vercel + Supabase + Cloudflare)
```bash
# 1. Set environment variables
export VERCEL_ENABLED=true
export SUPABASE_ENABLED=true
export CLOUDFLARE_ENABLED=true

export DATABASE_URL=postgresql://postgres:[PASSWORD]@db.project-id.supabase.co:5432/postgres
export SUPABASE_ANON_KEY=your_anon_key
export SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

export CLOUDFLARE_API_TOKEN=your_api_token
export CLOUDFLARE_ACCOUNT_ID=your_account_id
export CLOUDFLARE_WORKER_NAME=machine-native-ops-worker

# 2. Deploy frontend to Vercel
vercel --prod

# 3. Deploy backend to Cloudflare Workers
wrangler deploy

# 4. Set up database in Supabase
supabase db push

# 5. Test integration
curl https://your-app.vercel.app/api/health
```

---

## Troubleshooting

### Common Issues

#### Cloudflare Workers Not Responding
```bash
# Check worker logs
wrangler tail

# Verify worker deployment
wrangler deployments list

# Test worker locally
wrangler dev
```

#### Supabase Connection Issues
```bash
# Test database connection
psql $DATABASE_URL

# Check migration status
supabase migration list

# View database logs
supabase logs db
```

#### GitBook Sync Issues
```bash
# Check GitHub integration status
# Via GitBook web interface: Settings -> Integrations -> GitHub

# Manually trigger sync
# Via GitBook web interface: Sync now

# Check for conflicts
# Via GitBook web interface: Conflicts tab
```

---

## Best Practices

1. **Use Environment Variables**: Store all sensitive data in environment variables
2. **Enable Authentication**: Use Supabase Auth or Cloudflare Access for security
3. **Implement Monitoring**: Set up logging and monitoring for all services
4. **Use CDN**: Leverage Cloudflare CDN for static assets
5. **Database Optimization**: Use Supabase RLS for data security
6. **Documentation**: Keep GitBook documentation up to date
7. **Backup Strategy**: Regularly backup Supabase and Cloudflare R2 data
8. **Testing**: Test all integrations before production deployment

---

## Support

For issues or questions:
- GitHub Issues: https://github.com/MachineNativeOps/machine-native-ops/issues
- Documentation: https://docs.machine-native-ops.com
- Community: https://community.machine-native-ops.com