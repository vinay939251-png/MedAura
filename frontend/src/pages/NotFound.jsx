import { Link } from 'react-router-dom'

export default function NotFound() {
  return (
    <div className="not-found animate-fade-in">
      <h1>404</h1>
      <p>Page not found</p>
      <Link to="/" className="btn btn-primary">Back to Dashboard</Link>
    </div>
  )
}
