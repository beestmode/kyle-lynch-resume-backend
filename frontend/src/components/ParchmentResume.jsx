import React, { useState, useEffect } from 'react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Separator } from './ui/separator';
import { 
  Download, 
  Mail, 
  Phone, 
  Linkedin, 
  MapPin,
  Calendar,
  Building,
  GraduationCap,
  Briefcase,
  Star,
  Edit,
  Settings,
  LogOut
} from 'lucide-react';
import ContactForm from './ContactForm';
import EditExperienceModal from './EditExperienceModal';
import AdminLogin from './AdminLogin';
import { resumeAPI } from '../services/api';
import { useAuth } from './AuthContext';
import { useToast } from '../hooks/use-toast';

const ParchmentResume = () => {
  const [resumeData, setResumeData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showContact, setShowContact] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showAdminLogin, setShowAdminLogin] = useState(false);
  const [selectedExperience, setSelectedExperience] = useState(null);
  const [editingPersonal, setEditingPersonal] = useState(false);
  const [editingHighlights, setEditingHighlights] = useState(false);
  const [editingSkills, setEditingSkills] = useState(false);
  const [editingEducation, setEditingEducation] = useState(false);
  const { isAuthenticated, logout } = useAuth();
  const { toast } = useToast();

  // Load resume data on mount
  useEffect(() => {
    loadResumeData();
  }, []);

  const loadResumeData = async () => {
    try {
      setLoading(true);
      const data = await resumeAPI.getResume();
      setResumeData(data);
    } catch (error) {
      console.error('Error loading resume:', error);
      toast({
        title: "Error",
        description: "Failed to load resume data. Please try again.",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPDF = async () => {
    try {
      const pdfBlob = await resumeAPI.downloadPDF();
      
      // Create download link
      const url = window.URL.createObjectURL(pdfBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'Kyle_Lynch_Resume.pdf';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);

      toast({
        title: "Success",
        description: "Resume PDF downloaded successfully!",
      });
    } catch (error) {
      console.error('Error downloading PDF:', error);
      toast({
        title: "Error",
        description: "Failed to download PDF. Please try again.",
        variant: "destructive",
      });
    }
  };

  const handleEditExperience = (experience) => {
    if (!isAuthenticated) {
      setShowAdminLogin(true);
      return;
    }
    setSelectedExperience(experience);
    setShowEditModal(true);
  };

  const handleExperienceUpdated = () => {
    // Reload resume data after update
    loadResumeData();
    setShowEditModal(false);
    setSelectedExperience(null);
  };

  const handleAdminLoginSuccess = () => {
    toast({
      title: "Admin Access Granted",
      description: "You can now edit resume content.",
    });
  };

  const handleLogout = () => {
    logout();
  };

  // New edit handlers for different sections
  const handleUpdatePersonalInfo = async (personalData) => {
    try {
      await resumeAPI.updatePersonalInfo(personalData);
      loadResumeData();
      setEditingPersonal(false);
      toast({
        title: "Success",
        description: "Personal information updated successfully!",
      });
    } catch (error) {
      console.error('Error updating personal info:', error);
      toast({
        title: "Error",
        description: "Failed to update personal information.",
        variant: "destructive",
      });
    }
  };

  const handleUpdateHighlights = async (highlights) => {
    try {
      await resumeAPI.updateHighlights({ highlights });
      loadResumeData();
      setEditingHighlights(false);
      toast({
        title: "Success",
        description: "Highlights updated successfully!",
      });
    } catch (error) {
      console.error('Error updating highlights:', error);
      toast({
        title: "Error",
        description: "Failed to update highlights.",
        variant: "destructive",
      });
    }
  };

  const handleUpdateSkills = async (skills) => {
    try {
      await resumeAPI.updateSkills({ skills });
      loadResumeData();
      setEditingSkills(false);
      toast({
        title: "Success",
        description: "Skills updated successfully!",
      });
    } catch (error) {
      console.error('Error updating skills:', error);
      toast({
        title: "Error",
        description: "Failed to update skills.",
        variant: "destructive",
      });
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-amber-50 to-orange-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-amber-600 mx-auto mb-4"></div>
          <p className="text-amber-800 text-lg">Loading resume...</p>
        </div>
      </div>
    );
  }

  if (!resumeData) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-amber-50 to-orange-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-amber-800 text-lg">Failed to load resume data.</p>
          <Button 
            onClick={loadResumeData}
            className="mt-4 bg-amber-700 hover:bg-amber-800 text-cream"
          >
            Try Again
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-amber-50 to-orange-50 p-4">
      <div className="max-w-4xl mx-auto">
        {/* Admin Controls */}
        {isAuthenticated && (
          <div className="fixed top-4 right-4 z-30 flex gap-2">
            <Button
              size="sm"
              variant="outline"
              onClick={handleLogout}
              className="bg-amber-100 border-amber-300 text-amber-800 hover:bg-amber-200"
            >
              <LogOut className="w-4 h-4 mr-1" />
              Logout
            </Button>
          </div>
        )}

        {/* Parchment Paper Effect */}
        <div className="parchment-container relative bg-gradient-to-br from-yellow-50 via-amber-50 to-orange-100 shadow-2xl border border-amber-200 overflow-hidden">
          {/* Decorative Border */}
          <div className="absolute inset-4 border-2 border-amber-600 opacity-30 rounded-lg"></div>
          <div className="absolute inset-6 border border-amber-500 opacity-20 rounded-md"></div>
          
          {/* Main Content */}
          <div className="relative z-10 p-12">
            {/* Header Section */}
            <header className="text-center mb-12 border-b-2 border-amber-600 pb-8 relative">
              {isAuthenticated && (
                <Button
                  size="sm"
                  variant="ghost"
                  onClick={() => setEditingPersonal(true)}
                  className="absolute top-0 right-0 text-amber-700 hover:text-amber-900 hover:bg-amber-100"
                >
                  <Edit className="w-4 h-4" />
                </Button>
              )}
              <h1 className="text-5xl font-bold text-amber-900 mb-4 calligraphic-font tracking-wide">
                {resumeData.personal_info?.name || 'Kyle J. Lynch'}
              </h1>
              <p className="text-xl text-amber-800 mb-6 italic font-medium">
                {resumeData.personal_info?.title || 'Facilities Coordinator & Technical Systems Professional'}
              </p>
              
              {/* Contact Information */}
              <div className="flex flex-wrap justify-center gap-6 text-amber-800">
                <div className="flex items-center gap-2">
                  <Mail className="w-4 h-4" />
                  <a href={`mailto:${resumeData.personal_info?.email}`} 
                     className="hover:text-amber-900 transition-colors">
                    {resumeData.personal_info?.email}
                  </a>
                </div>
                <div className="flex items-center gap-2">
                  <Phone className="w-4 h-4" />
                  <span>{resumeData.personal_info?.phone}</span>
                </div>
                <div className="flex items-center gap-2">
                  <Linkedin className="w-4 h-4" />
                  <a href={resumeData.personal_info?.linkedin} 
                     target="_blank" 
                     rel="noopener noreferrer"
                     className="hover:text-amber-900 transition-colors">
                    LinkedIn Profile
                  </a>
                </div>
                <div className="flex items-center gap-2">
                  <MapPin className="w-4 h-4" />
                  <span>{resumeData.personal_info?.location}</span>
                </div>
              </div>
            </header>

            {/* Action Buttons */}
            <div className="flex justify-center gap-4 mb-12">
              <Button 
                onClick={handleDownloadPDF}
                className="bg-amber-700 hover:bg-amber-800 text-cream border border-amber-600 shadow-lg"
              >
                <Download className="w-4 h-4 mr-2" />
                Download PDF
              </Button>
              <Button 
                onClick={() => setShowContact(true)}
                variant="outline"
                className="border-amber-600 text-amber-800 hover:bg-amber-100"
              >
                <Mail className="w-4 h-4 mr-2" />
                Contact Me
              </Button>
              {!isAuthenticated && (
                <Button
                  onClick={() => setShowAdminLogin(true)}
                  variant="outline"
                  className="border-amber-600 text-amber-800 hover:bg-amber-100"
                >
                  <Settings className="w-4 h-4 mr-2" />
                  Admin
                </Button>
              )}
            </div>

            {/* Highlights Section */}
            <section className="mb-12 relative">
              <h2 className="text-2xl font-bold text-amber-900 mb-6 flex items-center gap-2">
                <Star className="w-6 h-6" />
                Highlights of Qualifications
                {isAuthenticated && (
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => setEditingHighlights(true)}
                    className="ml-auto text-amber-700 hover:text-amber-900 hover:bg-amber-100"
                  >
                    <Edit className="w-4 h-4" />
                  </Button>
                )}
              </h2>
              <div className="space-y-3">
                {resumeData.highlights?.map((highlight, index) => (
                  <div key={index} className="flex items-start gap-3">
                    <div className="w-2 h-2 bg-amber-600 rounded-full mt-3 flex-shrink-0"></div>
                    <p className="text-amber-800 text-lg leading-relaxed">{highlight}</p>
                  </div>
                ))}
              </div>
            </section>

            {/* Experience Section */}
            <section className="mb-12">
              <h2 className="text-2xl font-bold text-amber-900 mb-6 flex items-center gap-2">
                <Briefcase className="w-6 h-6" />
                Professional Experience
              </h2>
              
              <div className="space-y-8">
                {resumeData.experience?.map((exp, index) => (
                  <Card key={exp.id || index} className="bg-amber-50/50 border-amber-200 p-6 hover:shadow-lg transition-shadow">
                    <div className="flex justify-between items-start mb-4">
                      <div className="flex-grow">
                        <h3 className="text-xl font-bold text-amber-900 mb-1">
                          {exp.position}
                        </h3>
                        <div className="flex items-center gap-2 text-amber-700 mb-2">
                          <Building className="w-4 h-4" />
                          <span className="font-semibold">{exp.company}</span>
                          <span className="text-amber-600">•</span>
                          <span>{exp.location}</span>
                        </div>
                        <div className="flex items-center gap-2 text-amber-600 mb-3">
                          <Calendar className="w-4 h-4" />
                          <span className="italic">{exp.duration}</span>
                          {exp.current && (
                            <Badge className="bg-green-100 text-green-800 border-green-200">
                              Current
                            </Badge>
                          )}
                        </div>
                      </div>
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={() => handleEditExperience(exp)}
                        className="text-amber-600 hover:text-amber-800 hover:bg-amber-100"
                      >
                        <Edit className="w-4 h-4" />
                      </Button>
                    </div>
                    
                    <p className="text-amber-800 leading-relaxed mb-4">
                      {exp.description}
                    </p>
                    
                    {exp.achievements && exp.achievements.length > 0 && (
                      <div className="mt-4">
                        <h4 className="font-semibold text-amber-900 mb-2">Key Achievements:</h4>
                        <ul className="list-disc list-inside space-y-1">
                          {exp.achievements.map((achievement, idx) => (
                            <li key={idx} className="text-amber-800">{achievement}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </Card>
                ))}
              </div>
            </section>

            {/* Education Section */}
            <section className="mb-12">
              <h2 className="text-2xl font-bold text-amber-900 mb-6 flex items-center gap-2">
                <GraduationCap className="w-6 h-6" />
                Education & Certifications
                {isAuthenticated && (
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => setEditingEducation(true)}
                    className="ml-auto text-amber-700 hover:text-amber-900 hover:bg-amber-100"
                  >
                    <Edit className="w-4 h-4" />
                  </Button>
                )}
              </h2>
              
              <div className="grid gap-4 md:grid-cols-2">
                {resumeData.education?.map((edu) => (
                  <Card key={edu.id} className="bg-amber-50/50 border-amber-200 p-4">
                    <h3 className="font-bold text-amber-900 mb-1">{edu.degree}</h3>
                    <p className="text-amber-700 font-medium">{edu.institution}</p>
                    {edu.location && (
                      <p className="text-amber-600 text-sm">{edu.location}</p>
                    )}
                    <p className="text-amber-600 text-sm italic mt-1">{edu.duration}</p>
                  </Card>
                ))}
              </div>
            </section>

            {/* Skills Section */}
            <section>
              <h2 className="text-2xl font-bold text-amber-900 mb-6">
                Core Competencies
              </h2>
              <div className="flex flex-wrap gap-3">
                {resumeData.skills?.map((skill, index) => (
                  <Badge 
                    key={index}
                    className="bg-amber-100 text-amber-800 border-amber-300 px-4 py-2 text-sm font-medium hover:bg-amber-200 transition-colors"
                  >
                    {skill}
                  </Badge>
                ))}
              </div>
            </section>

            {/* Decorative Footer */}
            <div className="mt-16 text-center">
              <Separator className="bg-amber-600 mb-6" />
              <p className="text-amber-600 italic text-sm">
                Professional Resume of {resumeData.personal_info?.name || 'Kyle J. Lynch'}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Contact Modal */}
      {showContact && (
        <ContactForm 
          onClose={() => setShowContact(false)}
          recipientEmail={resumeData.personal_info?.email}
        />
      )}

      {/* Admin Login Modal */}
      {showAdminLogin && (
        <AdminLogin 
          onClose={() => setShowAdminLogin(false)}
          onSuccess={handleAdminLoginSuccess}
        />
      )}

      {/* Edit Experience Modal */}
      {showEditModal && selectedExperience && (
        <EditExperienceModal
          experience={selectedExperience}
          onClose={() => setShowEditModal(false)}
          onSave={handleExperienceUpdated}
        />
      )}
    </div>
  );
};

export default ParchmentResume;