from ..utils.__init__ import db

class Movie(db.Model):
    __tablename__='movies'

    id=db.Column(db.Integer(),primary_key=True)
    title = db.Column(db.String(30),nullable=False)
    director = db.Column(db.String(100),nullable=False)
    rating = db.Column(db.Float())
    year = db.Column(db.Integer)
    genre = db.Column(db.String(50))
    description = db.Column(db.String(300))

    def __str__(self):
        return f"<Movie {self.id}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()