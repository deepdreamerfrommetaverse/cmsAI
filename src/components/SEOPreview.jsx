export default function SEOPreview({ title, description }) {
  return (
    <div className="border border-gray-600 p-3 rounded-lg">
      <p className="text-blue-300">{title}</p>
      <p className="text-gray-400">{description}</p>
    </div>
  )
}
