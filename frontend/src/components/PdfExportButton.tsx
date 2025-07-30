import React from 'react';
import api from '../lib/api';

interface Props {
  articleId: number;
}

const PdfExportButton: React.FC<Props> = ({ articleId }) => {
  const handleExport = async () => {
    try {
      const res = await api.get(`/api/articles/${articleId}/export/pdf`, { responseType: 'blob' });
      // Create a download link for the PDF
      const url = window.URL.createObjectURL(new Blob([res.data], { type: 'application/pdf' }));
      const link = document.createElement('a');
      link.href = url;
      link.download = `article_${articleId}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (err) {
      console.error("PDF export failed", err);
      alert("Failed to export PDF.");
    }
  };
  return (
    <button onClick={handleExport} className="px-3 py-1 text-sm bg-primary text-white rounded hover:bg-primary-dark">
      Export PDF
    </button>
  );
};

export default PdfExportButton;
