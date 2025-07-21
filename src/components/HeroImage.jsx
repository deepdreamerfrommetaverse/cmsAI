export default function HeroImage({ src, alt }) {
  return (
    <img
      src={src}
      alt={alt}
      className="w-full max-h-60 object-cover rounded-xl"
    />
  )
}
