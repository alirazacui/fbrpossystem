/**
 * Format currency
 */
export const formatCurrency = (amount: number): string => {
  return new Intl.NumberFormat('en-PK', {
    style: 'currency',
    currency: 'PKR',
    minimumFractionDigits: 2,
  }).format(amount)
}

/**
 * Format date
 */
export const formatDate = (date: string | Date): string => {
  return new Intl.DateTimeFormat('en-PK', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(date))
}

/**
 * Format phone number (Pakistani format)
 */
export const formatPhoneNumber = (phone: string): string => {
  const cleaned = phone.replace(/\D/g, '')
  if (cleaned.length === 10) {
    return `(${cleaned.slice(0, 3)}) ${cleaned.slice(3, 6)}-${cleaned.slice(6)}`
  }
  return phone
}

/**
 * Truncate text
 */
export const truncateText = (text: string, maxLength: number): string => {
  return text.length > maxLength ? `${text.substring(0, maxLength)}...` : text
}

/**
 * Generate random ID
 */
export const generateId = (): string => {
  return Math.random().toString(36).substring(2, 11)
}

/**
 * Delay (for testing)
 */
export const delay = (ms: number): Promise<void> => {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

/**
 * Check if email is valid
 */
export const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

/**
 * Convert FBR status to readable text
 */
export const getFBRStatusLabel = (status: string): { label: string; color: string } => {
  const statusMap: Record<string, { label: string; color: string }> = {
    SUCCESS: { label: 'Submitted', color: 'green' },
    FAILED: { label: 'Failed', color: 'red' },
    PENDING: { label: 'Pending', color: 'yellow' },
  }
  return statusMap[status] || { label: 'Unknown', color: 'gray' }
}

/**
 * Convert sale status to readable text
 */
export const getSaleStatusLabel = (status: string): { label: string; color: string } => {
  const statusMap: Record<string, { label: string; color: string }> = {
    DRAFT: { label: 'Draft', color: 'gray' },
    COMPLETED: { label: 'Completed', color: 'green' },
    CANCELLED: { label: 'Cancelled', color: 'red' },
  }
  return statusMap[status] || { label: 'Unknown', color: 'gray' }
}
