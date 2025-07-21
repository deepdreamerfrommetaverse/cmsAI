export default function Card({ title, children }) {
  return (
    <div className="bg-gray-800 p-4 rounded-xl">
      {title && <h3 className="text-xl font-semibold mb-2">{title}</h3>}
      {children}
    </div>
  )
}
