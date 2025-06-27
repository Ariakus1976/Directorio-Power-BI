import React, { useState, useEffect } from 'react';
import './App.css';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

// Group color mapping for visual organization
const GROUP_COLORS = {
  'DIRECCION COMERCIAL': 'from-blue-500 to-blue-600',
  'COMERCIALES': 'from-green-500 to-green-600', 
  'COMPRAS': 'from-purple-500 to-purple-600',
  'RECURSOS HUMANOS': 'from-orange-500 to-orange-600',
  'GERENCIA': 'from-red-500 to-red-600',
  'SUCURSALES': 'from-teal-500 to-teal-600',
  'ALTEC': 'from-indigo-500 to-indigo-600'
};

const GROUP_ICONS = {
  'DIRECCION COMERCIAL': '📊',
  'COMERCIALES': '💼', 
  'COMPRAS': '🛒',
  'RECURSOS HUMANOS': '👥',
  'GERENCIA': '🏢',
  'SUCURSALES': '🏪',
  'ALTEC': '⚙️'
};

function App() {
  const [reports, setReports] = useState([]);
  const [filteredReports, setFilteredReports] = useState([]);
  const [groups, setGroups] = useState([]);
  const [selectedGroup, setSelectedGroup] = useState('ALL');
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState(null);
  const [error, setError] = useState(null);

  // Fetch data on component mount
  useEffect(() => {
    fetchData();
  }, []);

  // Filter reports when search term or selected group changes
  useEffect(() => {
    filterReports();
  }, [reports, selectedGroup, searchTerm]);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Fetch all data concurrently
      const [reportsResponse, groupsResponse, statsResponse] = await Promise.all([
        fetch(`${API_BASE_URL}/api/reports`),
        fetch(`${API_BASE_URL}/api/groups`),
        fetch(`${API_BASE_URL}/api/stats`)
      ]);

      if (!reportsResponse.ok || !groupsResponse.ok || !statsResponse.ok) {
        throw new Error('Failed to fetch data from server');
      }

      const reportsData = await reportsResponse.json();
      const groupsData = await groupsResponse.json();
      const statsData = await statsResponse.json();

      setReports(reportsData.data || []);
      setGroups(groupsData.data || []);
      setStats(statsData.data || null);

    } catch (err) {
      console.error('Error fetching data:', err);
      setError('Error al cargar los datos. Por favor, intenta de nuevo.');
    } finally {
      setLoading(false);
    }
  };

  const filterReports = () => {
    let filtered = reports;

    // Filter by group
    if (selectedGroup !== 'ALL') {
      filtered = filtered.filter(report => report.group === selectedGroup);
    }

    // Filter by search term
    if (searchTerm) {
      filtered = filtered.filter(report => 
        report.name.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    setFilteredReports(filtered);
  };

  const handleReportClick = (url) => {
    window.open(url, '_blank', 'noopener,noreferrer');
  };

  const getGroupCount = (groupName) => {
    if (!stats?.groups) return 0;
    const groupStat = stats.groups.find(g => g._id === groupName);
    return groupStat ? groupStat.count : 0;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600 text-lg">Cargando directorio de informes...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 flex items-center justify-center">
        <div className="text-center bg-white p-8 rounded-lg shadow-lg max-w-md">
          <div className="text-red-500 text-5xl mb-4">⚠️</div>
          <h2 className="text-xl font-semibold text-red-600 mb-2">Error de Conexión</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button 
            onClick={fetchData}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Reintentar
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Header */}
      <header className="bg-white shadow-lg border-b-4 border-blue-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="bg-gradient-to-r from-blue-600 to-blue-700 p-3 rounded-xl shadow-lg">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">Directorio Power BI</h1>
                <p className="text-gray-600 mt-1">Acceso centralizado a informes empresariales</p>
              </div>
            </div>
            {stats && (
              <div className="bg-blue-50 px-4 py-2 rounded-lg border border-blue-200">
                <span className="text-blue-800 font-semibold">{stats.total_reports} informes</span>
              </div>
            )}
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Search and Filter Controls */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-8 border border-gray-200">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0 lg:space-x-6">
            {/* Search Bar */}
            <div className="flex-1 max-w-md">
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
                <input
                  type="text"
                  placeholder="Buscar informes..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                />
              </div>
            </div>

            {/* Group Filter */}
            <div className="flex-1 max-w-sm">
              <select
                value={selectedGroup}
                onChange={(e) => setSelectedGroup(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors bg-white"
              >
                <option value="ALL">Todas las áreas ({reports.length})</option>
                {groups.map((group) => (
                  <option key={group} value={group}>
                    {GROUP_ICONS[group]} {group} ({getGroupCount(group)})
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Active Filters Display */}
          {(selectedGroup !== 'ALL' || searchTerm) && (
            <div className="mt-4 flex flex-wrap gap-2">
              {selectedGroup !== 'ALL' && (
                <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                  {GROUP_ICONS[selectedGroup]} {selectedGroup}
                  <button
                    onClick={() => setSelectedGroup('ALL')}
                    className="ml-2 inline-flex items-center justify-center w-4 h-4 rounded-full text-blue-400 hover:bg-blue-200 hover:text-blue-600"
                  >
                    ×
                  </button>
                </span>
              )}
              {searchTerm && (
                <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                  Búsqueda: "{searchTerm}"
                  <button
                    onClick={() => setSearchTerm('')}
                    className="ml-2 inline-flex items-center justify-center w-4 h-4 rounded-full text-green-400 hover:bg-green-200 hover:text-green-600"
                  >
                    ×
                  </button>
                </span>
              )}
            </div>
          )}
        </div>

        {/* Results Summary */}
        <div className="mb-6">
          <p className="text-gray-600">
            Mostrando <span className="font-semibold text-gray-900">{filteredReports.length}</span> de <span className="font-semibold text-gray-900">{reports.length}</span> informes
          </p>
        </div>

        {/* Reports Grid */}
        {filteredReports.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-gray-400 text-6xl mb-4">📊</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">No se encontraron informes</h3>
            <p className="text-gray-600 mb-4">
              {searchTerm ? 
                `No hay informes que coincidan con "${searchTerm}"` : 
                'No hay informes disponibles para los filtros seleccionados'
              }
            </p>
            {(searchTerm || selectedGroup !== 'ALL') && (
              <button
                onClick={() => {
                  setSearchTerm('');
                  setSelectedGroup('ALL');
                }}
                className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
              >
                Limpiar filtros
              </button>
            )}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filteredReports.map((report) => (
              <div
                key={report.id}
                onClick={() => handleReportClick(report.url)}
                className="bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 cursor-pointer border border-gray-200 hover:border-blue-300 transform hover:-translate-y-1 group"
              >
                {/* Report Header with Group Badge */}
                <div className={`bg-gradient-to-r ${GROUP_COLORS[report.group]} p-4 rounded-t-xl`}>
                  <div className="flex items-center justify-between">
                    <span className="text-white font-semibold text-sm bg-white bg-opacity-20 px-3 py-1 rounded-full">
                      {GROUP_ICONS[report.group]} {report.group}
                    </span>
                    <svg className="w-5 h-5 text-white opacity-75 group-hover:opacity-100 transition-opacity" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                    </svg>
                  </div>
                </div>

                {/* Report Content */}
                <div className="p-6">
                  {/* Power BI Icon */}
                  <div className="flex items-center justify-center w-16 h-16 bg-yellow-100 rounded-xl mb-4 mx-auto">
                    <svg className="w-10 h-10 text-yellow-600" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M14.5 2L12 4.5L14.5 7L17 4.5L14.5 2M9.5 7L7 9.5L9.5 12L12 9.5L9.5 7M14.5 12L12 14.5L14.5 17L17 14.5L14.5 12M4.5 7L2 9.5L4.5 12L7 9.5L4.5 7M9.5 17L7 19.5L9.5 22L12 19.5L9.5 17M19.5 7L17 9.5L19.5 12L22 9.5L19.5 7Z" />
                    </svg>
                  </div>

                  {/* Report Title */}
                  <h3 className="font-bold text-gray-900 text-lg mb-2 text-center leading-tight group-hover:text-blue-600 transition-colors">
                    {report.name}
                  </h3>

                  {/* Call to Action */}
                  <div className="text-center mt-4">
                    <span className="inline-flex items-center text-blue-600 font-semibold text-sm group-hover:text-blue-700 transition-colors">
                      Abrir informe
                      <svg className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7" />
                      </svg>
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <div className="flex items-center justify-center space-x-2 mb-4">
              <div className="bg-gradient-to-r from-blue-600 to-blue-700 p-2 rounded-lg">
                <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <span className="text-gray-700 font-semibold">Directorio Power BI</span>
            </div>
            <p className="text-gray-600">
              Plataforma centralizada para acceder a todos los informes de business intelligence
            </p>
            <p className="text-gray-500 text-sm mt-2">
              © 2024 - Directorio empresarial de informes Power BI
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;