module.exports = {
  purge: [],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        primarybgc: '#ececec',
        primarybgn: '#323232',
        primarybgh: '#232323',
        primarybgb: '#2a9fd6'
      },
      zIndex: {
        1040: '1040',
        '-1': '-1'
      },
      spacing: {
        100: '25rem',
        15: '3.75rem',
        292.5: '73.125rem',
        242.5: '60.625rem',
        187.5: '46.875rem'
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
