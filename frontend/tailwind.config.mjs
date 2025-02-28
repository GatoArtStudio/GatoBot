/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
      },
      boxShadow: {
        'neon': '0 0 5px theme("colors.blue.400"), 0 0 20px theme("colors.blue.700")',
        'neon-purple': '0 0 5px theme("colors.purple.400"), 0 0 20px theme("colors.purple.700")',
      },
    },
  },
  plugins: [],
}
