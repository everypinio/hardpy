# Frontend Database Routing Example

This example demonstrates how to configure separate database routing for backend and frontend when running HardPy in containerized environments.

## Use Case

When running HardPy in Docker containers, the backend and frontend often need different database connection strings:

- **Backend** (HardPy test runner) runs inside a container and connects to the database using Docker's internal networking (e.g., service name `couchdb`)
- **Frontend** (user's web browser) runs on the host machine and needs to connect using exposed ports (e.g., `localhost:5984` or external hostname)

## Configuration

The `hardpy.toml` file shows two database configurations:

```toml
# Backend uses Docker internal networking
[database]
host = "couchdb"  # Docker service name
port = 5984

# Frontend uses host-accessible address
[database_frontend]
host = "localhost"  # Accessible from browser
port = 5984
```

## When to Use This

Use separate database configurations when:

1. **Running in Docker/Kubernetes** - Backend and frontend use different network paths to the same database
2. **Using a Read Replica** - Frontend connects to a read-only replica for better performance
3. **Firewall/Network Separation** - Different network zones for test execution vs UI access
4. **Development Environments** - Backend in container, frontend accessed from host browser

## When NOT to Use This

If your setup doesn't need separate routing, simply omit the `[database_frontend]` section. HardPy will automatically use the `[database]` config for both backend and frontend.

## Example Docker Setup

The included `docker-compose.yaml` demonstrates a typical containerized setup where this configuration is needed.
