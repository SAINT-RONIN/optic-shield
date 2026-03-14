function snakeToCamel(str: string): string {
  return str.replace(/_([a-z])/g, (_, c: string) => c.toUpperCase())
}

function camelToSnake(str: string): string {
  return str.replace(/[A-Z]/g, (c) => `_${c.toLowerCase()}`)
}

export function transformKeys<T>(obj: unknown): T {
  if (Array.isArray(obj)) return obj.map(item => transformKeys(item)) as T
  if (obj !== null && typeof obj === 'object') {
    const result: Record<string, unknown> = {}
    for (const [key, value] of Object.entries(obj as Record<string, unknown>)) {
      result[snakeToCamel(key)] = transformKeys(value)
    }
    return result as T
  }
  return obj as T
}

export function toSnakeKeys<T>(obj: unknown): T {
  if (Array.isArray(obj)) return obj.map(item => toSnakeKeys(item)) as T
  if (obj !== null && typeof obj === 'object') {
    const result: Record<string, unknown> = {}
    for (const [key, value] of Object.entries(obj as Record<string, unknown>)) {
      result[camelToSnake(key)] = toSnakeKeys(value)
    }
    return result as T
  }
  return obj as T
}
