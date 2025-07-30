import React from "react";

interface BrickProps {
  block: any;
}

// This component would render a single block from the Bricks JSON layout.
// For simplicity, we'll just output based on type.
const BrickBlock: React.FC<BrickProps> = ({ block }) => {
  if (!block) return null;
  switch(block.type) {
    case 'heading':
      return <h2 className="text-xl font-bold my-2">{block.content}</h2>;
    case 'image':
      return <img src={block.src} alt={block.alt || 'Image'} className="my-4 max-w-full"/>;
    case 'text':
    default:
      return <p className="my-2">{block.content}</p>;
  }
};

export default BrickBlock;
