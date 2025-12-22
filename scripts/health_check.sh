#!/bin/bash
set -e

echo "🔍 Frontend typecheck"
npx tsc --noEmit

echo "🚀 Backend compile"
python -m compileall backend

echo "✅ All checks passed"