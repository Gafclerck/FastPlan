import click
from werkzeug.security import generate_password_hash

from app.repositories.user_repo import UserRepo
from app.validators.user_validator import UserValidator


def register_cli(app):
    @app.cli.command("create-manager")
    @click.option("--name", prompt="Prénom")
    @click.option("--surname", prompt="Nom")
    @click.option("--email", prompt="Email")
    @click.option(
        "--password",
        prompt=True,
        hide_input=True,
        confirmation_prompt=True,
        help="Mot de passe (min. 8 caractères)",
    )
    def create_manager(name, surname, email, password):
        """Crée un compte utilisateur avec le rôle gestionnaire (sans inscription publique)."""
        err_n = UserValidator.validate_name(name)
        if err_n:
            raise click.ClickException(err_n)
        err_s = UserValidator.validate_surname(surname)
        if err_s:
            raise click.ClickException(err_s)
        mail_err = UserValidator.validate_email(email)
        if mail_err:
            raise click.ClickException(mail_err)
        if not password or len(password) < 8:
            raise click.ClickException("Le mot de passe doit contenir au moins 8 caractères.")

        if UserRepo.getByEmail(email):
            raise click.ClickException("Cet email est déjà enregistré.")

        pwd_hash = generate_password_hash(password)
        try:
            uid = UserRepo.create_user(
                name=name,
                surname=surname,
                email=email,
                password_hash=pwd_hash,
                role="gestionnaire",
            )
        except Exception as exc:
            raise click.ClickException(f"Échec de la création : {exc}") from exc

        click.echo(f"Gestionnaire créé (id={uid}). Connexion avec : {email.strip().lower()}")
