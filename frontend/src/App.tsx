import { useEffect, useState } from 'react'

function App() {
  const [apiStatus, setApiStatus] = useState<string>('...')

  useEffect(() => {
    fetch('/api/health/')
      .then(res => res.json())
      .then(data => setApiStatus(data.status))
      .catch(() => setApiStatus('unreachable'))
  }, [])

  return (
    <div className="min-h-screen bg-gray-950 text-white flex flex-col items-center justify-center gap-4">
      <h1 className="text-4xl font-bold tracking-tight">CyberVeille</h1>
      <p className="text-gray-400 text-sm">
        API : <span className={apiStatus === 'ok' ? 'text-green-400' : 'text-red-400'}>{apiStatus}</span>
      </p>
    </div>
  )
}

export default App