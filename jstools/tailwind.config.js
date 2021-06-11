module.exports = {
  purge: [],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        primarybgc: '#ececec',
        primarybgn: '#323232',
        primarybgh: '#232323',
        primarybgb: '#2a9fd6',
        primarybgu: 'f9f9f9'
      },
      zIndex: {
        1040: '1040',
        '-1': '-1'
      },
      spacing: {
        15: '3.75rem',
        30: '7.5rem',
        90: '22.5rem',
        97.5: '24.375rem',
        100: '25rem',
        187.5: '46.875rem',
        195: '48.75rem',
        242.5: '60.625rem',
        292.5: '73.125rem'
      },
      width: (theme) => ({
        ...theme('spacing'),
        fullx3: '300%',
      }),
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
