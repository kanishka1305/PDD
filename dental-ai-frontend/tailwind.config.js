/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        navy: {
          950: '#030712',
          900: '#0a0e1a',
          800: '#0d1520',
          700: '#111827',
          600: '#1a2235',
          500: '#1e2d40',
          400: '#2a3a52',
        },
        brand: {
          DEFAULT: '#3b82f6',
          light: '#60a5fa',
          dark: '#1d4ed8',
        },
        emerald: { DEFAULT: '#10b981', light: '#34d399' },
        amber:   { DEFAULT: '#f59e0b', light: '#fbbf24' },
        rose:    { DEFAULT: '#ef4444', light: '#f87171' },
        cyan:    { DEFAULT: '#06b6d4', light: '#22d3ee' },
        violet:  { DEFAULT: '#8b5cf6', light: '#a78bfa' },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      boxShadow: {
        glass: '0 8px 32px rgba(0,0,0,0.4)',
        card:  '0 4px 24px rgba(0,0,0,0.3)',
        glow:  '0 0 20px rgba(59,130,246,0.3)',
      },
      backdropBlur: { glass: '12px' },
      borderRadius: { xl2: '1rem', xl3: '1.5rem' },
      animation: {
        'pulse-slow':  'pulse 3s ease-in-out infinite',
        'slide-up':    'slideUp 0.3s ease-out',
        'fade-in':     'fadeIn 0.4s ease-out',
      },
      keyframes: {
        slideUp:  { from: { opacity: '0', transform: 'translateY(12px)' }, to: { opacity: '1', transform: 'translateY(0)' } },
        fadeIn:   { from: { opacity: '0' }, to: { opacity: '1' } },
      },
    },
  },
  plugins: [],
}
