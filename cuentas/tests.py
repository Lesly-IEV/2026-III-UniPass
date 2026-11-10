from unittest.mock import patch

from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse

from bicicletas.models import Bicicleta
from cuentas.models import PerfilUsuario
from cuentas.permisos import ADMINISTRADOR, ALUMNO, GUARDIA, sincronizar_grupos


class ControlDeAccesoTests(TestCase):
    def setUp(self):
        sincronizar_grupos()
        self.alumno = self._cuenta("alumno1", ALUMNO, "A001")
        self.guardia = self._cuenta("guardia1", GUARDIA, "")
        self.admin = self._cuenta("admin1", ADMINISTRADOR, "")
        self.bici = Bicicleta.objects.create(
            usuario=self.alumno.perfil,
            numero_folio="F-1",
            marca="Benotto",
            color="Roja",
        )
        self.ajena = Bicicleta.objects.create(
            usuario=PerfilUsuario.objects.create(
                user=User.objects.create_user("otro", password="clave-segura-1"),
                matricula="A999",
            ),
            numero_folio="F-2",
            marca="Alubike",
            color="Negra",
        )
        self.ajena.usuario.user.groups.add(Group.objects.get(name=ALUMNO))

    def _cuenta(self, username, grupo, matricula):
        user = User.objects.create_user(username, password="clave-segura-1")
        user.groups.add(Group.objects.get(name=grupo))
        PerfilUsuario.objects.create(user=user, matricula=matricula or None)
        return user

    def test_alumno_no_escanea_ni_administra(self):
        self.client.force_login(self.alumno)
        self.assertEqual(self.client.get(reverse("verificar_acceso")).status_code, 302)
        self.assertEqual(self.client.get(reverse("lista_usuarios")).status_code, 302)
        self.assertEqual(self.client.get(reverse("registrar_bicicleta")).status_code, 302)
        self.assertEqual(self.client.get(reverse("historial_accesos")).status_code, 302)

    def test_alumno_solo_edita_su_bicicleta(self):
        self.client.force_login(self.alumno)
        self.assertEqual(self.client.get(reverse("editar_bicicleta", args=[self.bici.pk])).status_code, 200)
        self.assertEqual(self.client.get(reverse("editar_bicicleta", args=[self.ajena.pk])).status_code, 404)
        self.assertEqual(self.client.get(reverse("ver_qr", args=[self.bici.pk])).status_code, 200)
        self.assertEqual(self.client.get(reverse("ver_qr", args=[self.ajena.pk])).status_code, 404)

    def test_guardia_escanea_y_no_ve_bicicletas_ajenas(self):
        self.client.force_login(self.guardia)
        self.assertEqual(self.client.get(reverse("verificar_acceso")).status_code, 200)
        self.assertRedirects(self.client.get(reverse("mis_bicicletas")), reverse("verificar_acceso"))
        self.assertEqual(self.client.get(reverse("editar_bicicleta", args=[self.bici.pk])).status_code, 302)
        self.assertEqual(self.client.get(reverse("lista_usuarios")).status_code, 302)

    def test_guardia_registra_con_el_token_no_con_un_id(self):
        self.client.force_login(self.guardia)
        respuesta = self.client.post(
            reverse("verificar_acceso"),
            {"action": "registrar_entrada", "bicicleta_id": self.bici.pk, "codigo": "1"},
        )
        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(self.bici.accesos.count(), 0)

        self.client.post(
            reverse("verificar_acceso"),
            {"action": "registrar_entrada", "qr_token": str(self.bici.qr_token)},
        )
        self.assertEqual(self.bici.accesos.count(), 1)

    def test_admin_crea_la_vista_de_usuarios(self):
        self.client.force_login(self.admin)
        self.assertEqual(self.client.get(reverse("lista_usuarios")).status_code, 200)
        self.assertEqual(self.client.get(reverse("nuevo_usuario")).status_code, 200)

    def test_cerrar_sesion_exige_post(self):
        self.client.force_login(self.alumno)
        self.assertEqual(self.client.get(reverse("logout")).status_code, 405)
        self.assertEqual(self.client.post(reverse("logout")).status_code, 302)

    def test_registro_publico_no_existe(self):
        self.assertEqual(self.client.get("/registro/").status_code, 404)

    def test_sin_sesion_el_decorador_lleva_al_login(self):
        respuesta = self.client.get(reverse("verificar_acceso"))
        self.assertRedirects(respuesta, reverse("login"))

    def test_sin_grupo_el_decorador_niega_y_cierra_sesion(self):
        usuario = User.objects.create_user("sin-grupo", password="clave-segura-1")
        self.client.force_login(usuario)
        respuesta = self.client.get(reverse("verificar_acceso"))
        self.assertRedirects(respuesta, reverse("login"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_error_interno_al_leer_el_permiso_lleva_al_login(self):
        self.client.force_login(self.admin)
        with patch("django.contrib.auth.models.User.has_perm", side_effect=RuntimeError("fallo")):
            respuesta = self.client.get(reverse("lista_usuarios"))
        self.assertRedirects(respuesta, reverse("login"))
        self.assertNotIn("_auth_user_id", self.client.session)
