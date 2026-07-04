interface ImportMetaEnv {
  readonly VITE_API_BASE_URL?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

declare module '*.css'

declare namespace JSX {
  interface IntrinsicElements {
    [elementName: string]: any
  }
}

declare module 'react' {
  export type ReactNode = any
  export function useEffect(effect: () => void | (() => void), deps?: any[]): void
  export function useMemo<T>(factory: () => T, deps?: any[]): T
  export function useState<T>(initialState: T | (() => T)): [T, (value: T) => void]
  const React: { StrictMode: (props: { children?: ReactNode }) => any }
  export default React
}

declare module 'react/jsx-runtime' {
  export const jsx: any
  export const jsxs: any
  export const Fragment: any
}

declare module 'react-dom/client' {
  const ReactDOM: {
    createRoot: (element: HTMLElement) => { render: (node: any) => void }
  }
  export default ReactDOM
}

declare module 'react-router-dom' {
  export function BrowserRouter(props: { children?: any }): any
  export function Routes(props: { children?: any }): any
  export function Route(props: { path: string; element: any }): any
  export function Link(props: { to: string; children?: any; className?: string; style?: any }): any
  export function useParams(): Record<string, string | undefined>
}
