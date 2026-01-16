# Frontend Documentation

Comprehensive documentation for the My Domains Info frontend application.

## 📋 Overview

The frontend is a modern, single-page application built with Vue.js 3 that provides an intuitive web interface for managing and monitoring domain information. It communicates with the backend API to display domain data, handle domain additions, and refresh domain information.

## 🎯 Features

- **Domain Management**: Add and view domains with a clean, user-friendly interface
- **Real-time Data**: Automatic data fetching and caching with TanStack Query
- **Pagination**: Efficient pagination for large domain lists
- **Toast Notifications**: User-friendly error and success notifications
- **Responsive Design**: Modern UI built with Tailwind CSS
- **Type Safety**: Full TypeScript support throughout the application
- **Fast Development**: Hot module replacement with Vite

## 🏗 Technology Stack

### Core Framework
- **Vue.js 3.5+**: Progressive JavaScript framework with Composition API
- **TypeScript 5.9+**: Type-safe JavaScript for better developer experience
- **Vite (Rolldown)**: Next-generation build tool for fast development and optimized production builds

### State Management & Data Fetching
- **TanStack Query (Vue Query) 5.92+**: Powerful data synchronization library for Vue
  - Automatic caching and background updates
  - Request deduplication
  - Optimistic updates
  - Query invalidation

### Routing
- **Vue Router 4.6+**: Official router for Vue.js applications

### Styling
- **Tailwind CSS 4.1+**: Utility-first CSS framework
- **PostCSS**: CSS processing with autoprefixer

### Development Tools
- **Biome 2.3+**: Fast formatter and linter (replaces ESLint + Prettier)
- **vue-tsc**: TypeScript type checking for Vue SFCs
- **@vitejs/plugin-vue**: Vue SFC support for Vite

## 📁 Project Structure

```
frontend/
├── src/
│   ├── api/                    # API client functions
│   │   └── domain.ts          # Domain-related API calls
│   ├── assets/                 # Static assets (images, fonts, etc.)
│   ├── components/             # Reusable Vue components
│   │   ├── AddDomainModal.vue # Modal for adding new domains
│   │   ├── DomainTable.vue    # Table component for displaying domains
│   │   └── ToastContainer.vue # Toast notification container
│   ├── composables/            # Vue composition functions
│   │   ├── useDomainInfo.ts   # Domain data fetching composables
│   │   └── useToast.ts        # Toast notification composable
│   ├── pages/                  # Page components
│   │   └── DomainInfoPage.vue # Main domain information page
│   ├── types/                  # TypeScript type definitions
│   │   └── domain.ts          # Domain-related types
│   ├── views/                  # View components
│   │   └── HomeView.vue       # Home/landing view
│   ├── App.vue                 # Root component
│   ├── main.ts                 # Application entry point
│   ├── style.css               # Global styles
│   └── vite-env.d.ts           # Vite environment type definitions
├── public/                     # Public static assets
├── dist/                       # Production build output (generated)
├── biome.json                  # Biome linter/formatter configuration
├── package.json                # Dependencies and scripts
├── tsconfig.json               # TypeScript configuration
├── tsconfig.app.json           # TypeScript config for app code
├── tsconfig.node.json          # TypeScript config for Node.js tooling
└── vite.config.ts              # Vite build configuration
```

## 🚀 Getting Started

### Prerequisites

- **Node.js 24+** (or compatible version)
- **npm** or **yarn** package manager

### Installation

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Set up environment variables:**
   Create a `.env` file in the `frontend/` directory (optional):
   ```bash
   VITE_API_URL=http://localhost:8000/api
   ```

   > **Note:** If `VITE_API_URL` is not set, the app defaults to `http://localhost:8000/api`

### Development

Start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:5173` (or the next available port).

The dev server includes:
- **Hot Module Replacement (HMR)**: Instant updates without page refresh
- **Fast Refresh**: Preserves component state during updates
- **Source Maps**: Easy debugging in browser DevTools

### Building for Production

Build the application for production:

```bash
npm run build
```

This will:
- Type-check the code with `vue-tsc`
- Optimize and bundle the application with Vite
- Output files to `../static/` directory (for backend integration)

The build process:
- Minifies JavaScript and CSS
- Tree-shakes unused code
- Optimizes assets
- Generates source maps for production debugging

### Preview Production Build

Preview the production build locally:

```bash
npm run preview
```

This serves the built files from `../static/` to verify the production build works correctly.

## ⚙️ Configuration

### Environment Variables

The frontend uses Vite's environment variable system. Variables must be prefixed with `VITE_` to be exposed to the client code.

#### Available Variables

- **`VITE_API_URL`** (optional): Backend API URL
  - Default: `http://localhost:8000/api`
  - Format: Should end with `/api` (automatically normalized if not)
  - Example: `VITE_API_URL=http://localhost:8000/api`
  - Example: `VITE_API_URL=https://api.example.com/api`

#### Setting Environment Variables

**Development:**
Create a `.env` file in the `frontend/` directory:
```bash
VITE_API_URL=http://localhost:8000/api
```

**Production Build:**
Set the variable when building:
```bash
VITE_API_URL=https://your-api.com/api npm run build
```

Or use a `.env.production` file:
```bash
VITE_API_URL=https://your-api.com/api
```

### Vite Configuration

The Vite configuration (`vite.config.ts`) includes:

- **Path Aliases**: `@/` maps to `src/` directory
- **Vue Plugin**: Enables Vue SFC support
- **Build Output**: Configured to output to `../static/` for backend integration

### TypeScript Configuration

The project uses a composite TypeScript setup:

- **`tsconfig.json`**: Root configuration with project references
- **`tsconfig.app.json`**: Configuration for application code
- **`tsconfig.node.json`**: Configuration for Vite config and build tools

## 🏛️ Architecture

### Component Structure

The application follows Vue 3 Composition API patterns:

- **Single File Components (SFC)**: `.vue` files with `<script setup>`, `<template>`, and `<style>`
- **Composition API**: Modern Vue 3 API for better code organization
- **TypeScript**: Full type safety throughout

### Data Flow

```
User Interaction
    ↓
Component (Vue)
    ↓
Composable (useDomainInfo, useToast)
    ↓
API Client (domain.ts)
    ↓
Backend API
    ↓
TanStack Query (caching, state management)
    ↓
Component (reactive updates)
```

### State Management

**TanStack Query** handles all server state:

- **Queries**: For fetching domain data (`useDomains`)
- **Mutations**: For adding/refreshing domains (`useAddDomain`, `useRefreshDomains`)
- **Cache Management**: Automatic caching and invalidation
- **Background Updates**: Automatic refetching on window focus (disabled by default)

**Local State** is managed with Vue's `ref` and `computed`:

- Component-specific state (e.g., current page, modal visibility)
- Derived state (e.g., total pages, loading states)

### API Integration

The API client (`src/api/domain.ts`) provides:

- **`fetchDomains(page, limit)`**: Get paginated domain list
- **`addDomain(domain)`**: Add a new domain
- **`refreshDomains()`**: Refresh all domain information

All functions include:
- Error handling with detailed messages
- Type-safe request/response handling
- Development logging

### Composables

**`useDomainInfo.ts`**:
- `useDomains(page)`: Query hook for fetching domains
- `useAddDomain()`: Mutation hook for adding domains
- `useRefreshDomains()`: Mutation hook for refreshing domains

**`useToast.ts`**:
- `showToast(message, type)`: Display toast notifications
- `removeToast(id)`: Remove a toast
- `toasts`: Reactive array of active toasts

## 🎨 Styling

### Tailwind CSS

The application uses Tailwind CSS 4.1+ for styling:

- **Utility Classes**: Rapid UI development with utility classes
- **Dark Mode**: Built-in dark mode support via `color-scheme`
- **Responsive Design**: Mobile-first responsive utilities
- **Custom Styles**: Additional styles in `style.css` for global overrides

### Custom Styles

Global styles are defined in `src/style.css`:

- CSS custom properties for theming
- Base typography and layout styles
- Dark mode color scheme
- Button and form element styles

## 🔧 Development Workflow

### Code Quality

**Linting:**
```bash
npm run lint:check  # Check for linting issues
npm run lint        # Fix linting issues automatically
```

**Type Checking:**
```bash
npm run build       # Includes type checking via vue-tsc
```

### Biome Configuration

The project uses Biome for linting and formatting:

- **Linting**: Catches common errors and enforces best practices
- **Formatting**: Consistent code style across the project
- **Configuration**: See `biome.json` for rules and settings

Key Biome rules:
- Enforces self-closing elements
- Prevents parameter reassignment
- Disables exhaustive dependencies (for Vue composables)
- Allows non-null assertions where needed

### Development Best Practices

1. **Component Organization**:
   - Keep components focused and single-purpose
   - Extract reusable logic into composables
   - Use TypeScript for all new code

2. **API Integration**:
   - Always use the API client functions in `src/api/`
   - Handle errors gracefully with user-friendly messages
   - Use TanStack Query for all server state

3. **Styling**:
   - Prefer Tailwind utility classes
   - Use custom CSS only when necessary
   - Maintain consistent spacing and typography

4. **Type Safety**:
   - Define types in `src/types/` directory
   - Use TypeScript interfaces for API responses
   - Avoid `any` types (configured in Biome)

## 📦 Building for Production

### Build Process

1. **Type Checking**: `vue-tsc -b` validates all TypeScript code
2. **Bundling**: Vite optimizes and bundles the application
3. **Output**: Files are written to `../static/` directory

### Build Configuration

The build is configured in `vite.config.ts`:

- **Output Directory**: `../static/` (for backend integration)
- **Empty Output**: Cleans the output directory before building
- **Optimization**: Automatic code splitting and tree-shaking

### Production Considerations

- **API URL**: Ensure `VITE_API_URL` is set correctly for production
- **Environment Variables**: All `VITE_*` variables are embedded at build time
- **Asset Optimization**: Vite automatically optimizes images and assets
- **Bundle Size**: Monitor bundle size with `npm run build -- --report`

## 🔌 API Integration

### API Client

The API client (`src/api/domain.ts`) handles all backend communication:

**Base URL Configuration:**
- Reads from `VITE_API_URL` environment variable
- Defaults to `http://localhost:8000/api` if not set
- Automatically normalizes URL to end with `/api`

**Error Handling:**
- Extracts error messages from API responses
- Provides fallback error messages
- Throws typed errors for composables to handle

### API Endpoints

**GET `/api/domain-info/`**
- Fetches paginated domain list
- Query parameters: `limit`, `offset`
- Returns: `PaginatedDomainsResponse`

**POST `/api/domain-info/`**
- Adds a new domain
- Body: `{ domain_name: string }`
- Returns: `DomainInfo[]` (includes discovered subdomains)

**POST `/api/domain-info/refresh`**
- Refreshes all domain information
- Returns: `{ status: "ok" }`

### Type Definitions

Domain-related types are defined in `src/types/domain.ts`:

```typescript
interface DomainInfo {
  domain_name: string
  ip_address?: string | null
  dns_settings?: Record<string, string[]> | null
  geo_city?: string | null
  geo_country?: string | null
  network_owner_name?: string | null
  is_anycast_node: boolean
  is_active?: boolean | null
}

interface PaginatedDomainsResponse {
  items: DomainInfo[]
  total: number
}
```

## 🧪 Testing

While the project doesn't currently include a test suite, consider adding:

- **Unit Tests**: Vitest for component and composable testing
- **E2E Tests**: Playwright or Cypress for end-to-end testing
- **Component Tests**: Vue Test Utils for component testing

## 🐛 Troubleshooting

### Common Issues

**API Connection Errors:**
- Verify `VITE_API_URL` is set correctly
- Check that the backend is running
- Ensure CORS is configured on the backend

**Build Errors:**
- Run `npm run lint:check` to find linting issues
- Check TypeScript errors with `vue-tsc --noEmit`
- Clear `node_modules` and reinstall: `rm -rf node_modules && npm install`

**Type Errors:**
- Ensure all types are properly imported
- Check `src/types/` for type definitions
- Verify API response types match backend schema

**Styling Issues:**
- Verify Tailwind classes are correct
- Check `style.css` for global overrides
- Ensure PostCSS is processing Tailwind directives

### Development Server Issues

**Port Already in Use:**
- Vite will automatically try the next available port
- Or specify a port: `npm run dev -- --port 3000`

**Hot Reload Not Working:**
- Check browser console for errors
- Try hard refresh (Ctrl+Shift+R / Cmd+Shift+R)
- Restart the dev server

## 📚 Additional Resources

- [Vue.js Documentation](https://vuejs.org/)
- [Vite Documentation](https://vitejs.dev/)
- [TanStack Query (Vue)](https://tanstack.com/query/latest/docs/vue/overview)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [TypeScript Documentation](https://www.typescriptlang.org/)
- [Biome Documentation](https://biomejs.dev/)

## 🤝 Contributing

When contributing to the frontend:

1. Follow the existing code style (enforced by Biome)
2. Use TypeScript for all new code
3. Write composables for reusable logic
4. Keep components focused and small
5. Test your changes in both development and production builds
6. Update this documentation if adding new features

---

**Built with ❤️ using Vue.js, TypeScript, and modern web technologies**
