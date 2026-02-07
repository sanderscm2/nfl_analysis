'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

const navItems = [
  { href: '/', label: 'League Overview' },
  { href: '/teams', label: 'Team Analysis' },
  { href: '/players', label: 'Player Stats' },
  { href: '/analyze', label: 'Custom Analysis' },
  { href: '/insights', label: 'AI Insights' },
]

export default function Navigation() {
  const pathname = usePathname()

  return (
    <nav className="border-b border-gray-200 bg-white">
      <div className="max-w-7xl mx-auto">
        <ul className="flex gap-0">
          {navItems.map(item => {
            const isActive = pathname === item.href
            return (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className={isActive ? 'nav-link-active' : 'nav-link'}
                >
                  {item.label}
                </Link>
              </li>
            )
          })}
        </ul>
      </div>
    </nav>
  )
}
