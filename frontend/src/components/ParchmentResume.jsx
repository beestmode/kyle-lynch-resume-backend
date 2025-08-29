import React, { useState } from 'react';
import { resumeData } from '../data/mock';
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
  Edit
} from 'lucide-react';
import ContactForm from './ContactForm';
import EditExperienceModal from './EditExperienceModal';

const ParchmentResume = () => {
  const [showContact, setShowContact] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [selectedExperience, setSelectedExperience] = useState(null);

  const handleDownloadPDF = () => {
    // Mock download functionality
    const link = document.createElement('a');
    link.href = '/api/resume/download-pdf';
    link.download = 'Kyle_Lynch_Resume.pdf';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleEditExperience = (experience) => {
    setSelectedExperience(experience);
    setShowEditModal(true);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-amber-50 to-orange-50 p-4">
      <div className="max-w-4xl mx-auto">
        {/* Parchment Paper Effect */}
        <div className="parchment-container relative bg-gradient-to-br from-yellow-50 via-amber-50 to-orange-100 shadow-2xl border border-amber-200 overflow-hidden">
          {/* Decorative Border */}
          <div className="absolute inset-4 border-2 border-amber-600 opacity-30 rounded-lg"></div>
          <div className="absolute inset-6 border border-amber-500 opacity-20 rounded-md"></div>
          
          {/* Main Content */}
          <div className="relative z-10 p-12">
            {/* Header Section */}
            <header className="text-center mb-12 border-b-2 border-amber-600 pb-8">
              <h1 className="text-5xl font-bold text-amber-900 mb-4 calligraphic-font tracking-wide">
                {resumeData.personalInfo.name}
              </h1>
              <p className="text-xl text-amber-800 mb-6 italic font-medium">
                {resumeData.personalInfo.title}
              </p>
              
              {/* Contact Information */}
              <div className="flex flex-wrap justify-center gap-6 text-amber-800">
                <div className="flex items-center gap-2">
                  <Mail className="w-4 h-4" />
                  <a href={`mailto:${resumeData.personalInfo.email}`} 
                     className="hover:text-amber-900 transition-colors">
                    {resumeData.personalInfo.email}
                  </a>
                </div>
                <div className="flex items-center gap-2">
                  <Phone className="w-4 h-4" />
                  <span>{resumeData.personalInfo.phone}</span>
                </div>
                <div className="flex items-center gap-2">
                  <Linkedin className="w-4 h-4" />
                  <a href={resumeData.personalInfo.linkedin} 
                     target="_blank" 
                     rel="noopener noreferrer"
                     className="hover:text-amber-900 transition-colors">
                    LinkedIn Profile
                  </a>
                </div>
                <div className="flex items-center gap-2">
                  <MapPin className="w-4 h-4" />
                  <span>{resumeData.personalInfo.location}</span>
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
            </div>

            {/* Highlights Section */}
            <section className="mb-12">
              <h2 className="text-2xl font-bold text-amber-900 mb-6 flex items-center gap-2">
                <Star className="w-6 h-6" />
                Highlights of Qualifications
              </h2>
              <div className="space-y-3">
                {resumeData.highlights.map((highlight, index) => (
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
                {resumeData.experience.map((exp, index) => (
                  <Card key={exp.id} className="bg-amber-50/50 border-amber-200 p-6 hover:shadow-lg transition-shadow">
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
                    
                    {exp.achievements && (
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
              </h2>
              
              <div className="grid gap-4 md:grid-cols-2">
                {resumeData.education.map((edu) => (
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
                {resumeData.skills.map((skill, index) => (
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
                Professional Resume of {resumeData.personalInfo.name}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Contact Modal */}
      {showContact && (
        <ContactForm 
          onClose={() => setShowContact(false)}
          recipientEmail={resumeData.personalInfo.email}
        />
      )}

      {/* Edit Experience Modal */}
      {showEditModal && selectedExperience && (
        <EditExperienceModal
          experience={selectedExperience}
          onClose={() => setShowEditModal(false)}
          onSave={(updatedExp) => {
            // Mock save functionality
            console.log('Updated experience:', updatedExp);
            setShowEditModal(false);
          }}
        />
      )}
    </div>
  );
};

export default ParchmentResume;