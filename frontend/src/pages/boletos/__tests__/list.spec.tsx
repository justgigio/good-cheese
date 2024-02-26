import { describe, it, expect } from 'vitest'

import { render, screen } from '@testing-library/react'
import { Home } from '@/pages/home'

describe('Home', () => {
  it('renders the App component', () => {
    render(<Home />)
    // Failing for BUN reason... =/
  })
})