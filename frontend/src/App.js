import React, { useState, useEffect } from 'react';
import './App.css';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

// Power BI Usage Metrics URL
const POWERBI_METRICS_URL = 'https://app.powerbi.com/groups/cdb9df2c-4dfa-4824-888d-26de261e1c52/reports/1fe1bfbc-c42d-4292-86e0-e7ffb54037d7/a04359c48f27001e9786?experience=power-bi';

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

// Admin Modal Component
const AdminModal = ({ isOpen, onClose, onRefresh }) => {
  const [activeTab, setActiveTab] = useState('add');
  const [reports, setReports] = useState([]);
  const [groups, setGroups] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState('');

  // Form states
  const [newReport, setNewReport] = useState({ name: '', group: '', url: '' });
  const [editingReport, setEditingReport] = useState(null);
  const [newGroup, setNewGroup] = useState('');

  useEffect(() => {
    if (isOpen) {
      fetchAdminData();
    }
  }, [isOpen]);

  const fetchAdminData = async () => {
    try {
      const [reportsRes, groupsRes] = await Promise.all([
        fetch(`${API_BASE_URL}/api/reports`),
        fetch(`${API_BASE_URL}/api/groups`)
      ]);
      
      const reportsData = await reportsRes.json();
      const groupsData = await groupsRes.json();
      
      setReports(reportsData.data || []);
      setGroups(groupsData.data || []);
    } catch (error) {
      showMessage('Error al cargar datos', 'error');
    }
  };

  const showMessage = (msg, type) => {
    setMessage(msg);
    setMessageType(type);
    setTimeout(() => setMessage(''), 3000);
  };

  const handleCreateReport = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/admin/reports`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newReport)
      });
      
      const data = await response.json();
      
      if (data.success) {
        showMessage('Informe creado exitosamente', 'success');
        setNewReport({ name: '', group: '', url: '' });
        fetchAdminData();
        onRefresh();
      } else {
        showMessage(data.detail || 'Error al crear el informe', 'error');
      }
    } catch (error) {
      showMessage('Error de conexión', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateReport = async (e) => {
    e.preventDefault();
    if (!editingReport) return;
    
    setLoading(true);
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/admin/reports/${editingReport.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: editingReport.name,
          group: editingReport.group,
          url: editingReport.url
        })
      });
      
      const data = await response.json();
      
      if (data.success) {
        showMessage('Informe actualizado exitosamente', 'success');
        setEditingReport(null);
        fetchAdminData();
        onRefresh();
      } else {
        showMessage(data.detail || 'Error al actualizar el informe', 'error');
      }
    } catch (error) {
      showMessage('Error de conexión', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteReport = async (reportId, reportName) => {
    if (!window.confirm(`¿Estás seguro de que quieres eliminar el informe "${reportName}"?`)) {
      return;
    }
    
    setLoading(true);
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/admin/reports/${reportId}`, {
        method: 'DELETE'
      });
      
      const data = await response.json();
      
      if (data.success) {
        showMessage('Informe eliminado exitosamente', 'success');
        fetchAdminData();
        onRefresh();
      } else {
        showMessage(data.detail || 'Error al eliminar el informe', 'error');
      }
    } catch (error) {
      showMessage('Error de conexión', 'error');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-2xl w-full max-w-4xl max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white p-6">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold">Administración de Informes</h2>
            <button 
              onClick={onClose}
              className="text-white hover:text-gray-200 transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        {/* Message */}
        {message && (
          <div className={`p-4 m-4 rounded-lg ${messageType === 'success' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
            {message}
          </div>
        )}

        {/* Tabs */}
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6">
            {[
              { id: 'add', label: 'Agregar Informe', icon: '➕' },
              { id: 'manage', label: 'Gestionar Informes', icon: '📝' },
              { id: 'groups', label: 'Grupos', icon: '📁' }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-2 border-b-2 font-medium text-sm transition-colors ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                {tab.icon} {tab.label}
              </button>
            ))}
          </nav>
        </div>

        {/* Content */}
        <div className="p-6 max-h-[60vh] overflow-y-auto">
          {/* Add Report Tab */}
          {activeTab === 'add' && (
            <form onSubmit={handleCreateReport} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Nombre del Informe *
                </label>
                <input
                  type="text"
                  required
                  value={newReport.name}
                  onChange={(e) => setNewReport({...newReport, name: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Ej: Análisis de Ventas Q1"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Grupo/Área *
                </label>
                <select
                  required
                  value={newReport.group}
                  onChange={(e) => setNewReport({...newReport, group: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="">Seleccionar grupo...</option>
                  {groups.map((group) => (
                    <option key={group} value={group}>{group}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  URL de Power BI *
                </label>
                <input
                  type="url"
                  required
                  value={newReport.url}
                  onChange={(e) => setNewReport({...newReport, url: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="https://app.powerbi.com/groups/..."
                />
                <p className="text-xs text-gray-500 mt-1">
                  Debe ser una URL válida de app.powerbi.com
                </p>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
              >
                {loading ? 'Creando...' : 'Crear Informe'}
              </button>
            </form>
          )}

          {/* Manage Reports Tab */}
          {activeTab === 'manage' && (
            <div className="space-y-4">
              {reports.length === 0 ? (
                <p className="text-gray-500 text-center py-8">No hay informes para gestionar</p>
              ) : (
                reports.map((report) => (
                  <div key={report.id} className="border border-gray-200 rounded-lg p-4">
                    {editingReport?.id === report.id ? (
                      <form onSubmit={handleUpdateReport} className="space-y-4">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Nombre</label>
                            <input
                              type="text"
                              value={editingReport.name}
                              onChange={(e) => setEditingReport({...editingReport, name: e.target.value})}
                              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                            />
                          </div>
                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Grupo</label>
                            <select
                              value={editingReport.group}
                              onChange={(e) => setEditingReport({...editingReport, group: e.target.value})}
                              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                            >
                              {groups.map((group) => (
                                <option key={group} value={group}>{group}</option>
                              ))}
                            </select>
                          </div>
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">URL</label>
                          <input
                            type="url"
                            value={editingReport.url}
                            onChange={(e) => setEditingReport({...editingReport, url: e.target.value})}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                          />
                        </div>
                        <div className="flex space-x-2">
                          <button
                            type="submit"
                            disabled={loading}
                            className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 disabled:opacity-50"
                          >
                            Guardar
                          </button>
                          <button
                            type="button"
                            onClick={() => setEditingReport(null)}
                            className="bg-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-400"
                          >
                            Cancelar
                          </button>
                        </div>
                      </form>
                    ) : (
                      <div className="flex items-center justify-between">
                        <div className="flex-1">
                          <h3 className="font-semibold text-gray-900">{report.name}</h3>
                          <p className="text-sm text-gray-600">{report.group}</p>
                        </div>
                        <div className="flex space-x-2">
                          <button
                            onClick={() => setEditingReport(report)}
                            className="text-blue-600 hover:text-blue-800 p-1"
                            title="Editar"
                          >
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                            </svg>
                          </button>
                          <button
                            onClick={() => handleDeleteReport(report.id, report.name)}
                            className="text-red-600 hover:text-red-800 p-1"
                            title="Eliminar"
                          >
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                            </svg>
                          </button>
                        </div>
                      </div>
                    )}
                  </div>
                ))
              )}
            </div>
          )}

          {/* Groups Tab */}
          {activeTab === 'groups' && (
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Crear Nuevo Grupo</h3>
                <div className="flex space-x-2">
                  <input
                    type="text"
                    value={newGroup}
                    onChange={(e) => setNewGroup(e.target.value)}
                    placeholder="Nombre del nuevo grupo"
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                  <button
                    onClick={async () => {
                      if (!newGroup.trim()) return;
                      try {
                        const response = await fetch(`${API_BASE_URL}/api/admin/groups`, {
                          method: 'POST',
                          headers: { 'Content-Type': 'application/json' },
                          body: JSON.stringify({ name: newGroup })
                        });
                        const data = await response.json();
                        if (data.success) {
                          showMessage('Grupo creado exitosamente', 'success');
                          setNewGroup('');
                          fetchAdminData();
                        } else {
                          showMessage(data.detail || 'Error al crear el grupo', 'error');
                        }
                      } catch (error) {
                        showMessage('Error de conexión', 'error');
                      }
                    }}
                    className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
                  >
                    Crear
                  </button>
                </div>
              </div>

              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Grupos Existentes</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {groups.map((group) => (
                    <div key={group} className="bg-gray-50 p-4 rounded-lg flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <span className="text-2xl">{GROUP_ICONS[group] || '📁'}</span>
                        <span className="font-medium">{group}</span>
                      </div>
                      <span className="text-sm text-gray-500">
                        {reports.filter(r => r.group === group).length} informes
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
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
  const [showAdmin, setShowAdmin] = useState(false);

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

  const handleMetricsClick = () => {
    window.open(POWERBI_METRICS_URL, '_blank', 'noopener,noreferrer');
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
            
            <div className="flex items-center space-x-4">
              {/* Metrics Button */}
              <button
                onClick={handleMetricsClick}
                className="bg-gradient-to-r from-green-500 to-green-600 text-white px-4 py-2 rounded-lg hover:from-green-600 hover:to-green-700 transition-all duration-200 shadow-md hover:shadow-lg flex items-center space-x-2"
                title="Ver métricas de uso de Power BI"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                <span className="hidden sm:block">Métricas de Uso</span>
              </button>

              {/* Admin Button */}
              <button
                onClick={() => setShowAdmin(true)}
                className="bg-gradient-to-r from-purple-500 to-purple-600 text-white px-4 py-2 rounded-lg hover:from-purple-600 hover:to-purple-700 transition-all duration-200 shadow-md hover:shadow-lg flex items-center space-x-2"
                title="Administrar informes"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <span className="hidden sm:block">Administrar</span>
              </button>

              {/* Stats Display */}
              {stats && (
                <div className="bg-blue-50 px-4 py-2 rounded-lg border border-blue-200">
                  <span className="text-blue-800 font-semibold">{stats.total_reports} informes</span>
                </div>
              )}
            </div>
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
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-4">
            {filteredReports.map((report) => (
              <div
                key={report.id}
                onClick={() => handleReportClick(report.url)}
                className="bg-white rounded-lg shadow-md hover:shadow-lg transition-all duration-200 cursor-pointer border border-gray-200 hover:border-blue-300 transform hover:-translate-y-1 group"
              >
                {/* Report Header with Group Badge */}
                <div className={`bg-gradient-to-r ${GROUP_COLORS[report.group]} p-3 rounded-t-lg`}>
                  <div className="flex items-center justify-between">
                    <span className="text-white font-medium text-xs bg-white bg-opacity-20 px-2 py-1 rounded-full truncate">
                      {GROUP_ICONS[report.group]} {report.group}
                    </span>
                    <svg className="w-4 h-4 text-white opacity-75 group-hover:opacity-100 transition-opacity flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                    </svg>
                  </div>
                </div>

                {/* Report Content */}
                <div className="p-4">
                  {/* Report Title with Arrow */}
                  <div className="flex items-center justify-between">
                    <h3 className="font-semibold text-gray-900 text-sm leading-tight group-hover:text-blue-600 transition-colors flex-1 pr-2">
                      {report.name}
                    </h3>
                    <svg className="w-4 h-4 text-gray-400 group-hover:text-blue-600 group-hover:translate-x-1 transition-all flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7" />
                    </svg>
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

      {/* Admin Modal */}
      <AdminModal 
        isOpen={showAdmin} 
        onClose={() => setShowAdmin(false)} 
        onRefresh={fetchData}
      />
    </div>
  );
}

export default App;