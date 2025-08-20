import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import { Card, CardContent, CardHeader, CardTitle } from './components/ui/card';
import { Button } from './components/ui/button';
import { Input } from './components/ui/input';
import { Label } from './components/ui/label';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from './components/ui/dialog';
import { Textarea } from './components/ui/textarea';
import { Trash2, Edit, Plus, Users, Info, Home, Code2 } from 'lucide-react';

const API_URL = process.env.REACT_APP_BACKEND_URL;

function App() {
  const [showSplash, setShowSplash] = useState(true);
  const [currentSection, setCurrentSection] = useState('home');
  const [teamMembers, setTeamMembers] = useState([]);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [editingMember, setEditingMember] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    role: '',
    photo: '',
    description: ''
  });

  useEffect(() => {
    // Splash screen animation
    const timer = setTimeout(() => {
      setShowSplash(false);
    }, 3000);
    return () => clearTimeout(timer);
  }, []);

  useEffect(() => {
    fetchTeamMembers();
  }, []);

  const fetchTeamMembers = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/team-members`);
      setTeamMembers(response.data);
    } catch (error) {
      console.error('Error fetching team members:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingMember) {
        await axios.put(`${API_URL}/api/team-members/${editingMember.id}`, formData);
      } else {
        await axios.post(`${API_URL}/api/team-members`, formData);
      }
      fetchTeamMembers();
      setIsDialogOpen(false);
      setEditingMember(null);
      setFormData({ name: '', role: '', photo: '', description: '' });
    } catch (error) {
      console.error('Error saving team member:', error);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this member?')) {
      try {
        await axios.delete(`${API_URL}/api/team-members/${id}`);
        fetchTeamMembers();
      } catch (error) {
        console.error('Error deleting team member:', error);
      }
    }
  };

  const handleEdit = (member) => {
    setEditingMember(member);
    setFormData({
      name: member.name,
      role: member.role,
      photo: member.photo,
      description: member.description || ''
    });
    setIsDialogOpen(true);
  };

  const handleAddNew = () => {
    setEditingMember(null);
    setFormData({ name: '', role: '', photo: '', description: '' });
    setIsDialogOpen(true);
  };

  if (showSplash) {
    return (
      <div className="splash-screen">
        <div className="splash-content">
          <div className="code-symbol">
            <span className="bracket">&lt;</span>
            <span className="slash">/</span>
            <span className="bracket">&gt;</span>
          </div>
          <div className="club-info">
            <h1 className="club-name">Developer Students Club</h1>
            <h2 className="institute-name">SRM IST RMP</h2>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      {/* Header Navigation */}
      <header className="header">
        <div className="header-content">
          <div className="logo-section">
            <Code2 className="logo-icon" />
            <div className="logo-text">
              <span className="club-title">DSC</span>
              <span className="institute-subtitle">SRM IST RMP</span>
            </div>
          </div>
          
          <nav className="navigation">
            <button 
              className={`nav-item ${currentSection === 'home' ? 'active' : ''}`}
              onClick={() => setCurrentSection('home')}
            >
              <Home size={18} />
              <span>Home</span>
            </button>
            <button 
              className={`nav-item ${currentSection === 'about' ? 'active' : ''}`}
              onClick={() => setCurrentSection('about')}
            >
              <Info size={18} />
              <span>About</span>
            </button>
            <button 
              className={`nav-item ${currentSection === 'team' ? 'active' : ''}`}
              onClick={() => setCurrentSection('team')}
            >
              <Users size={18} />
              <span>Team</span>
            </button>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="main-content">
        {/* Home Section */}
        {currentSection === 'home' && (
          <section className="home-section">
            <div className="hero-content">
              <div className="hero-icon">
                <div className="code-symbol-large">
                  <span className="bracket">&lt;</span>
                  <span className="slash">/</span>
                  <span className="bracket">&gt;</span>
                </div>
              </div>
              <h1 className="hero-title">Developer Students Club</h1>
              <h2 className="hero-subtitle">SRM Institute of Science and Technology</h2>
              <h3 className="hero-campus">Ramapuram Campus</h3>
              <p className="hero-description">
                Empowering the next generation of developers through collaborative learning, 
                innovative projects, and community building.
              </p>
              <div className="hero-actions">
                <Button 
                  onClick={() => setCurrentSection('about')} 
                  className="cta-button"
                >
                  Learn More
                </Button>
                <Button 
                  onClick={() => setCurrentSection('team')} 
                  variant="outline" 
                  className="cta-button-outline"
                >
                  Meet Our Team
                </Button>
              </div>
            </div>
          </section>
        )}

        {/* About Section */}
        {currentSection === 'about' && (
          <section className="about-section">
            <div className="section-content">
              <div className="section-header">
                <h2 className="section-title">About Our Club</h2>
                <div className="title-underline"></div>
              </div>
              
              <div className="about-content">
                <Card className="about-card">
                  <CardContent className="about-card-content">
                    <div className="about-icon">
                      <Code2 size={48} />
                    </div>
                    <h3 className="about-card-title">Our Mission</h3>
                    <p className="about-text">
                      Developer Students Club at SRM IST Ramapuram is a community-driven initiative 
                      that aims to help students bridge the gap between theory and practice. We provide 
                      a platform for students to learn, grow, and build solutions for real-world problems 
                      using Google technologies and beyond.
                    </p>
                  </CardContent>
                </Card>

                <Card className="about-card">
                  <CardContent className="about-card-content">
                    <div className="about-icon">
                      <Users size={48} />
                    </div>
                    <h3 className="about-card-title">What We Do</h3>
                    <p className="about-text">
                      We organize workshops, hackathons, and study jams focused on emerging technologies. 
                      Our members work on innovative projects, participate in open-source contributions, 
                      and develop technical skills through hands-on experience with cutting-edge tools 
                      and frameworks.
                    </p>
                  </CardContent>
                </Card>

                <Card className="about-card">
                  <CardContent className="about-card-content">
                    <div className="about-icon">
                      <div className="code-symbol-small">
                        <span className="bracket">&lt;</span>
                        <span className="slash">/</span>
                        <span className="bracket">&gt;</span>
                      </div>
                    </div>
                    <h3 className="about-card-title">Join Us</h3>
                    <p className="about-text">
                      Whether you're a beginner eager to learn or an experienced developer looking to 
                      share knowledge, DSC SRM IST RMP welcomes everyone. Together, we create an 
                      inclusive environment where innovation thrives and friendships are forged 
                      through shared passion for technology.
                    </p>
                  </CardContent>
                </Card>
              </div>
            </div>
          </section>
        )}

        {/* Team Section */}
        {currentSection === 'team' && (
          <section className="team-section">
            <div className="section-content">
              <div className="section-header">
                <h2 className="section-title">Our Team</h2>
                <div className="title-underline"></div>
                <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
                  <DialogTrigger asChild>
                    <Button onClick={handleAddNew} className="add-member-button">
                      <Plus size={18} />
                      Add Member
                    </Button>
                  </DialogTrigger>
                  <DialogContent className="member-dialog">
                    <DialogHeader>
                      <DialogTitle>
                        {editingMember ? 'Edit Member' : 'Add New Member'}
                      </DialogTitle>
                    </DialogHeader>
                    <form onSubmit={handleSubmit} className="member-form">
                      <div className="form-group">
                        <Label htmlFor="name">Name</Label>
                        <Input
                          id="name"
                          value={formData.name}
                          onChange={(e) => setFormData({...formData, name: e.target.value})}
                          required
                        />
                      </div>
                      <div className="form-group">
                        <Label htmlFor="role">Role</Label>
                        <Input
                          id="role"
                          value={formData.role}
                          onChange={(e) => setFormData({...formData, role: e.target.value})}
                          required
                        />
                      </div>
                      <div className="form-group">
                        <Label htmlFor="photo">Photo URL</Label>
                        <Input
                          id="photo"
                          value={formData.photo}
                          onChange={(e) => setFormData({...formData, photo: e.target.value})}
                          placeholder="https://example.com/photo.jpg"
                        />
                      </div>
                      <div className="form-group">
                        <Label htmlFor="description">Description (Optional)</Label>
                        <Textarea
                          id="description"
                          value={formData.description}
                          onChange={(e) => setFormData({...formData, description: e.target.value})}
                          placeholder="Brief description about the member..."
                        />
                      </div>
                      <Button type="submit" className="submit-button">
                        {editingMember ? 'Update Member' : 'Add Member'}
                      </Button>
                    </form>
                  </DialogContent>
                </Dialog>
              </div>
              
              <div className="team-grid">
                {teamMembers.length === 0 ? (
                  <div className="empty-state">
                    <Users size={64} />
                    <h3>No team members yet</h3>
                    <p>Add your first team member to get started!</p>
                  </div>
                ) : (
                  teamMembers.map((member) => (
                    <Card key={member.id} className="member-card">
                      <CardContent className="member-card-content">
                        <div className="member-photo">
                          {member.photo ? (
                            <img src={member.photo} alt={member.name} />
                          ) : (
                            <div className="photo-placeholder">
                              <Users size={32} />
                            </div>
                          )}
                        </div>
                        <div className="member-info">
                          <h3 className="member-name">{member.name}</h3>
                          <p className="member-role">{member.role}</p>
                          {member.description && (
                            <p className="member-description">{member.description}</p>
                          )}
                        </div>
                        <div className="member-actions">
                          <Button
                            onClick={() => handleEdit(member)}
                            size="sm"
                            variant="outline"
                            className="action-button"
                          >
                            <Edit size={16} />
                          </Button>
                          <Button
                            onClick={() => handleDelete(member.id)}
                            size="sm"
                            variant="outline"
                            className="action-button delete-button"
                          >
                            <Trash2 size={16} />
                          </Button>
                        </div>
                      </CardContent>
                    </Card>
                  ))
                )}
              </div>
            </div>
          </section>
        )}
      </main>

      {/* Footer */}
      <footer className="footer">
        <div className="footer-content">
          <div className="footer-info">
            <div className="footer-logo">
              <Code2 size={24} />
              <span>DSC SRM IST RMP</span>
            </div>
            <p className="footer-text">
              Building the developer community, one project at a time.
            </p>
          </div>
          <div className="footer-links">
            <p className="footer-copyright">
              © 2024 Developer Students Club - SRM IST Ramapuram
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;