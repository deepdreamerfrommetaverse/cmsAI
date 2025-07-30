import React from "react";

interface Props {
  diffText: string;
  onClose: () => void;
  onConfirm: () => void;
}

const ConflictModal: React.FC<Props> = ({ diffText, onClose, onConfirm }) => {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-white dark:bg-gray-800 p-4 rounded w-11/12 max-w-lg">
        <h2 className="text-xl font-bold mb-2">Content Conflict Detected</h2>
        <p className="text-sm mb-4">The content has been modified externally. Differences:</p>
        <pre className="bg-gray-100 dark:bg-gray-900 p-2 text-xs overflow-auto mb-4">{diffText}</pre>
        <div className="text-right space-x-2">
          <button onClick={onClose} className="px-4 py-2 bg-gray-300 dark:bg-gray-700 rounded">Cancel</button>
          <button onClick={onConfirm} className="px-4 py-2 bg-primary text-white rounded">Overwrite</button>
        </div>
      </div>
    </div>
  );
};

export default ConflictModal;
