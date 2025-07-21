export default function Button({ children, ...props }) {
  return (
    <button
      {...props}
      className="px-3 py-2 rounded-lg bg-monday hover:bg-blue-600 disabled:opacity-50"
    >
      {children}
    </button>
  )
}
